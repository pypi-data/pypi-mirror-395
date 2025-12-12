"""
* `Organization`:  InsightSolver Solutions Inc.
* `Project Name`:  InsightSolver
* `Module Name`:   insightsolver
* `File Name`:     insightsolver.py
* `Author`:        Noé Aubin-Cadot
* `Email`:         noe.aubin-cadot@insightsolver.com

Description
-----------
This file contains the ``InsightSolver`` class.
This class is meant to ingest data, specify rule mining parameters and make rule mining API calls.

Note
----
A service key is necessary to use the API client.

License
-------
Exclusive Use License - see `LICENSE <license.html>`_ for details.

----------------------------

"""

################################################################################
################################################################################
# Define some global variables

API_SOURCE_PUBLIC = '-5547756002485302797'
# This string can be shared to customers of DSI as it refers to the public rule mining API.
# It is not tied with a specific user but is only a code that means 'public user outside DSI'.

################################################################################
################################################################################
# Import some libraries

import pandas as pd
import numpy as np
from requests.models import Response
from typing import Optional, Union, Dict, Sequence
import numbers
import mpmath # Useful for when the p-values are very small
from collections.abc import Mapping # To make the InsightSolver behave like a mapping like a dict

################################################################################
################################################################################
# Printing settings

#pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 12)
pd.set_option('max_colwidth', 20)
pd.set_option('display.width', 1000)

# Since numpy 2.0.0 printing numbers show their type but it makes reading results quickly harder.
# We revert to the legacy way of printing numbers.
if np.__version__>='2.0.0':
    legacy = '1.25'
else:
    legacy = None
np.set_printoptions(
    #linewidth = np.inf,
    #precision = 20,
    #precision = 1,
    #threshold = sys.maxsize,
    legacy = legacy,
)

################################################################################
################################################################################
# Defining some utilities

def compute_admissible_btypes(
    M:int,
    dtype:str,
    nunique:int,
    name:str,
):
    """
    This function computes the admissible `btypes` a column can take.
    The `btypes`:

    - ``'binary'``
    - ``'multiclass'``
    - ``'continuous'``
    - ``'ignore'``
    """
    # Import some functions
    from pandas.api.types import (
        pandas_dtype,
        is_numeric_dtype,
        is_integer_dtype,
        is_float_dtype,
        is_bool_dtype,
        is_datetime64_any_dtype,
        is_datetime64tz_dtype,
        is_timedelta64_dtype,
        is_categorical_dtype,
        is_string_dtype,
        is_object_dtype,
    )

    if is_bool_dtype(dtype):
        return [
            'binary',
            'ignore',
        ]
    elif is_numeric_dtype(dtype)\
        |is_datetime64_any_dtype(dtype)\
        |isinstance(pandas_dtype(dtype), pd.DatetimeTZDtype)\
        |is_timedelta64_dtype(dtype):
        if nunique<=2:
            return [
                'binary',
                'multiclass',
                'continuous',
                'ignore',
            ]
        else:
            return [
                #'binary',
                'multiclass',
                'continuous',
                'ignore',
            ]
    elif isinstance(pandas_dtype(dtype), pd.CategoricalDtype)\
        |is_object_dtype(dtype)\
        |is_string_dtype(dtype):
        if nunique<=2:
            return [
                'binary',
                'multiclass',
                #'continuous',
                'ignore',
            ]
        elif nunique<M:
            return [
                #'binary',
                'multiclass',
                'continuous',
                'ignore',
            ]
        else:
            return [
                #'binary',
                #'multiclass',
                'continuous',
                'ignore',
            ]
    else:
        print(f"WARNING: The variable='{name}' has a dtype='{dtype}' which is not handled yet. This variable is set to ignore.")
        return [
            #'binary',
            #'multiclass',
            #'continuous',
            'ignore',
        ]

def compute_columns_names_to_admissible_btypes(
    df: pd.DataFrame,
)->dict[str,list[str]]:
    """
    This function computes a dict that maps the column names of ``df`` to lists of admissible btypes.
    """
    # Take the dtype and nunique per column:
    s_dtype        = df.dtypes       # Pandas Series that maps column_name -> dtype
    s_nunique      = df.nunique()    # Pandas Series that maps column_name -> nunique
    s_contains_nan = df.isna().any() # Pandas Series that maps column_name -> if it contains a NaN
    M              = len(df)         # Number of rows
    # Convert to a Pandas DataFrame
    list_of_Series = (s_dtype,s_nunique,s_contains_nan)
    df_dtype_nunique = pd.concat(list_of_Series,axis=1).rename(columns={0:'dtype',1:'nunique',2:'contains_nan'})
    # Compute a dict that maps column_name -> btype
    columns_names_to_admissible_btypes = df_dtype_nunique.apply(lambda x:compute_admissible_btypes(M=M,dtype=x['dtype'],nunique=x['nunique'],name=x.name),axis=1).to_dict()
    # Return the result
    return columns_names_to_admissible_btypes

def validate_class_integrity(
    df: Optional[pd.DataFrame],            # DataFrame that'll be used to fit the solver
    target_name: Optional[Union[str,int]], # Target variable (must be a column of df)
    target_goal: Optional[Union[str,numbers.Real,np.uint8]], # Target goal
    columns_types: Optional[Dict],         # The specified types of the columns
    columns_descr:Optional[Dict],          # The textual descriptions of the columns
    threshold_M_max: Optional[int],        # The threshold on the maximum number of points to consider (must be a strictly positive integer)
    specified_constraints: Optional[Dict], # The specified constraints
    top_N_rules: Optional[int],            # The top N rules (must be a strictly positive integer)
    filtering_score: str,                  # The filtering score (must be a legit string)
    n_benchmark_original: int,             # To benchmark against random permutations (must be at least 2)
    n_benchmark_shuffle: int,              # To benchmark against random permutations (must be at least 2)
    do_strict_types: bool = False,         # If we want a strict evaluation of types
    verbose: bool = False,                 # Verbosity
)->dict:
    """
    This function validates the integrity of the parameter values passed during the instantiation of the InsightSolver class.

    Parameters
    ----------
    df: DataFrame
        The DataFrame that contains the data to analyse (a target column and various feature columns).
    target_name: str
        Name of the column of the target variable.
    target_goal: str (or other modality of the target variable)
        Target goal.
    columns_types: dict
        Types of the columns.
    columns_descr: dict
        Descriptions of the columns.
    threshold_M_max: int
        Threshold on the maximum number of observations to consider, above which we sample observations.
    specified_constraints: dict
        Dictionary of the specified constraints on m_min, m_max, coverage_min, coverage_max.
    top_N_rules: int
        An integer that specifies the maximum number of rules to get from the rule mining.
    filtering_score: str
        A string that specifies the filtering score to be used when selecting rules.
    n_benchmark_original: int
        An integer that specifies the number of benchmarking runs to execute where the target is not shuffled.
    n_benchmark_shuffle: int
        An integer that specifies the number of benchmarking runs to execute where the target is shuffled.
    do_strict_types: bool (default False)
        A boolean that specifies if we want a strict evaluation of types.
    verbose: bool (default False)
        Verbosity.

    Returns
    -------
    columns_types: dict
        A dict of the columns types after adjusting the types.
    """
    if verbose:
        print("Validating the integrity of the class...")

    # Validate that target_name is a column of df
    if target_name not in df.columns:
        raise Exception(f"ERROR (validate_class_integrity): target_name='{target_name}' not in df.columns.")
    # Make sure the target column does not contain missing values
    if df[target_name].isna().any():
        raise Exception(f"ERROR (validate_class_integrity): The target column target_name='{target_name}' contains {df[target_name].isna().sum()} missing values, but it should not contain missing values.")

    # Compute the admissible btypes per column
    columns_names_to_admissible_btypes = compute_columns_names_to_admissible_btypes(
        df = df,
    )
    
    # Make sure we have a dict of types
    if columns_types==None:
        # Create a dict
        columns_types = dict()
    else:
        # Make a copy to avoid editing it in-place
        columns_types = columns_types.copy()
    # Validate the columns types
    if columns_types!=None:
        # First, we make sure that the keys are legit
        # Take the set of valid keys
        keys_valid = set(df.columns)
        # Take the set of provided keys
        keys_present = columns_types.keys()
        # Look at if some keys are illegal
        keys_illegal = keys_present-keys_valid
        # If some keys are illegal
        if len(keys_illegal)>0:
            raise Exception(f"ERROR (columns_types invalid): some keys are illegal: {keys_illegal}.")
        # Loop over the dict of specified types
        for column_name,column_type in columns_types.items():
            # Make sure that the column_name is in df
            if column_name not in df.columns:
                raise Exception(f"ERROR (columns_types invalid): the dict 'columns_types' contains the column_name='{column_name}' but it is not a column of df.")
            # Make sure that the column_type is legit
            legit_btypes = ['binary','multiclass','continuous','ignore']
            if column_type not in legit_btypes:
                raise Exception(f"ERROR (columns_types invalid): the column='{column_name}' cannot be of type='{column_type}' because it must be in ['binary','multiclass','continuous','ignore'].")
            # Make sure that the column_type is admissible
            admissible_btypes = columns_names_to_admissible_btypes[column_name]
            if column_type not in admissible_btypes:
                if do_strict_types:
                    # If we are strict about the types, raise an exception
                    raise Exception(f"ERROR (columns_types invalid): the column_name='{column_name}' is specified as a column_type='{column_type}' but it is not a valid value in {admissible_btypes}.")
                else:
                    # If we are not strict about the types, substitute the type to 'ignore'
                    columns_types[column_name] = 'ignore'
            else:
                # Keep the provided type
                columns_types[column_name] = column_type

    # Validate that the target is not ignored
    if target_name in columns_types.keys():
        # Take the target type
        target_type = columns_types[target_name]
        # If the target type is 'ignore' there's a problem
        if target_type=='ignore':
            raise Exception(f"ERROR: target_name='{target_name}' is specified as 'ignore'.")

    # Validate that not all features are ignored
    features_types = columns_types.copy()
    if target_name in features_types.keys():
        features_types.pop(target_name)
    M,n=df.shape
    if (len(features_types)==n-1)&(all(features_types[column_name]=='ignore' for column_name in features_types.keys())):
        raise Exception("ERROR (columns_types): The specified type of each feature is 'ignore'.")

    # Validate columns_descr
    if columns_descr!=None:
        # Take the set of valid keys
        keys_valid = set(df.columns)
        # Take the set of provided keys
        keys_present = columns_descr.keys()
        # Look at if some keys are illegal
        keys_illegal = keys_present-keys_valid
        # If some keys are illegal
        if len(keys_illegal)>0:
            raise Exception(f"ERROR (columns_descr): some keys are illegal: {keys_illegal}.")

    # Validate threshold_M_max
    if threshold_M_max!=None:
        if threshold_M_max<=0:
            raise Exception(f"ERROR (threshold_M_max): threshold_M_max must be a strictly positive number, not {threshold_M_max}.")

    # Validate the specified_constraints
    if isinstance(specified_constraints, dict):
        # Take the set of valid keys
        keys_valid = {
            'm_min',
            'm_max',
            'coverage_min',
            'coverage_max',
            'mu_rule_min',
            'mu_rule_max',
            'lift_min',
            'lift_max',
        }
        # Take the set of keys present in the dict
        keys_present = specified_constraints.keys()
        # Look at if some keys are illegal
        keys_illegal = keys_present-keys_valid
        # If some keys are illegal
        if len(keys_illegal)>0:
            raise Exception(f"ERROR (specified_constraints): some keys are illegal: {keys_illegal}.")

    # Validate the top_N_rules
    if top_N_rules!=None:
        if top_N_rules<=0:
            raise Exception(f"ERROR (top_N_rules): The parameter top_N_rules must be a strictly positive integer. The value {top_N_rules} is invalid.")

    # Validate the filtering_score
    if filtering_score!='auto':
        valid_scores = ['lift','coverage','p_value','F_score','Z_score','TPR','PPV']
        scores = filtering_score.split('&')
        invalid_scores = sorted(set(scores)-set(valid_scores))
        if len(invalid_scores)>0:
            raise Exception(f"ERROR (filtering_score): The filtering score is not valid because it contains these scores: {invalid_scores}.")

    # Validate n_benchmark_original
    if n_benchmark_original<2:
        raise Exception(f"ERROR (n_benchmark_original): The parameter n_benchmark_original must be an integer >= 2.")
    
    # Validate n_benchmark_original
    if n_benchmark_shuffle<2:
        raise Exception(f"ERROR (n_benchmark_shuffle): The parameter n_benchmark_shuffle must be an integer >= 2.")

    # Validate target_goal
    target_modalities = df[target_name].unique()
    if target_goal in target_modalities:
        # If the target goal is in the modalities of the target variable, there is no problem
        if target_name not in columns_types.keys():
            if len(target_modalities)==0:
                raise Exception(f"ERROR: There is no modality in the target variable.")
            if len(target_modalities)==1:
                raise Exception(f"ERROR: There is only one modality in the target variable: '{target_modalities[0]}' (of type '{type(target_modalities[0]).__name__}').")
            elif len(target_modalities)==2:
                columns_types[target_name] = 'binary'
            else:
                columns_types[target_name] = 'multiclass'
    else:
        # If the target goal is not in the modalities of the target variable
        if isinstance(target_goal,str):
            # If the target goal is not in the target modalities but nevertheless is a string, we assume that the target type is 'continuous'
            # We make sure that the target_goal is legit for a continuous target variable
            import re
            if target_goal in ['min','max']:
                ...
            elif target_goal[:3] not in ['min','max']:
                raise Exception(f"ERROR: target_goal='{target_goal}' (of type '{type(target_goal).__name__}') is not a modality of the target variable. Therefore the target_goal string must start either with 'min' or 'max', not '{target_goal[:3]}'.")
            elif len(target_goal)<6:
                raise Exception(f"ERROR: target_goal='{target_goal}' (of type '{type(target_goal).__name__}') is not a modality of the target variable. The length of the target_goal string must be at least 6, not {len(target_goal)}.")
            elif target_goal[3]!='_':
                raise Exception(f"ERROR: target_goal='{target_goal}' (of type '{type(target_goal).__name__}') is not a modality of the target variable. If the 4th character of the string target_goal is specified it must be '_', not '{target_goal[3]}'.")
            elif re.match(r"^min_q[0-3]{1}$", target_goal)!=None:
                # If it's 'min' with a quartile 0, 1, 2, 3, it's ok (but 4 is not).
                ...
            elif re.match(r"^min_c[0-9]{2}$", target_goal)!=None:
                # If it's 'min' with a centile 00, 01, 02, ..., 98, 99.
                ...
            elif re.match(r"^max_q[1-4]{1}$", target_goal)!=None:
                # If it's 'max' with a quartile 1, 2, 3, 4, it's ok (but 0 is not).
                ...
            elif re.match(r"^max_c[0-9]{2}$", target_goal)!=None:
                # If it's 'max' with a 00, 01, 02, ..., 98, 99.
                if target_goal=='max_c00':
                    raise Exception(f"ERROR: target_goal='{target_goal}' is not a valid string.")
            elif re.match(r"^max_c100$",      target_goal)!=None:
                # If it's 'max' with a centile 100.
                ...
            else:
                raise Exception(f"ERROR: target_goal='{target_goal}' is not a valid string.")
            # We make sure that the target type is continuous
            if target_name in columns_types.keys():
                if columns_types[target_name]!='continuous':
                    raise Exception(f"ERROR: The target_goal='{target_goal}' indicates that the target variable '{target_name}' is 'continuous' but the specified type is '{columns_types[target_name]}'. Please either choose another type for the target variable or choose another target goal.")
            else:
                columns_types[target_name] = 'continuous'
        else:
            # If it's not a string, we raise an exception
            target_modalities = sorted(target_modalities)
            if len(target_modalities)<=10:
                error_message = f"ERROR: target_goal='{target_goal}' (of type '{type(target_goal).__name__}') is neither a valid string (like 'min' or 'max' etc.) nor a modality of target_modalities='{target_modalities}'."
            else:
                error_message = f"ERROR: target_goal='{target_goal}' (of type '{type(target_goal).__name__}') is neither a valid string (like 'min' or 'max' etc.) nor a modality of target_modalities:"
                for modality in target_modalities[:3]:
                    error_message+= f'\n\t{modality}'
                error_message+= '\n\t...'
                for modality in target_modalities[-3:]:
                    error_message+= f'\n\t{modality}'
            raise Exception(error_message)

    # At this point the type of the target variable should be known
    if target_name not in columns_types.keys():
        raise Exception("ERROR: The type of the target variable is not specified.")

    # Return the modified types
    return columns_types

def format_value(
    value,
    format_type = 'scientific', # 'scientific', 'percentage', 'scientific_no_decimals'
    decimals    = 1,
    verbose     = False,
):
    """
    This function formats values depending on the type of values (``float`` or ``mpmath``) and the type of the format to show:

    - ``'percentage'``: shows the values as percentage (default).
    - ``'scientific'``: shows the values in scientific notation with 4 decimals.
    - ``'scientific_no_decimals'``: shows the values in scientific notation without decimals.
    """
    if pd.isna(value):
        return ''

    if isinstance(value, mpmath.mpf):
        if value>1e-320:
            if verbose:
                print(f"The value mpmath {value} > 1e-320 is converted to float, no need to keep mpmath.")
            value = float(value)
    
    if format_type == 'percentage':
        if isinstance(value, mpmath.mpf):
            return f"{mpmath.nstr(value * 100, n=1+decimals, strip_zeros=True)}%"
        elif isinstance(value, float):
            return f"{value * 100:.{decimals}f}%"    
    elif format_type == 'scientific':
        if isinstance(value, mpmath.mpf):
            return mpmath.nstr(value, n=1+decimals, strip_zeros=False)
        elif isinstance(value, float):
            return f'{value:.{decimals}e}'
    elif format_type == 'scientific_no_decimals':
        if isinstance(value, mpmath.mpf):
            result = mpmath.nstr(value, n=1, strip_zeros=False)
            if '.e' in result:
                result = result.replace('.e', 'e')
            return result
        elif isinstance(value, float):
            return f"{value:.0e}"
    else:
        return value

def S_to_index_points_in_rule(
    solver,
    S:dict,
    verbose:bool              = False,
    df:Optional[pd.DataFrame] = None,
)->pd.Index:
    """
    This function takes a rule ``S`` and returns the index of the points inside the rule of a DataFrame.
    If no DataFrame is provided, the one used to train the solver is used.
    """
    if verbose:
        print('S :',S)
    # Create a temporary DataFrame that will be iteratively filtered
    if isinstance(df,pd.DataFrame):
        # If df is specified, we take it
        df_features_filtre = df.copy()
        # Since df is specified there is no reason that it contains all modalities
        all_modalities_should_be_present = False
    else:
        # If df is not specified, we take the DataFrame in the solver
        df_features_filtre = solver.df.copy()
        # Since df is from the solver, it should contain all the modalities
        all_modalities_should_be_present = True
    # Take the features names in the rule S
    feature_names = list(S.keys())
    # Make sure that the names are legit
    feature_names_illegal = set(feature_names)-set(solver.df.columns)
    if len(feature_names_illegal)>0:
        raise Exception(f"ERROR: there are illegal names in the rule S : {feature_names_illegal}.")
    # Sort the features names from the rule S
    feature_names.sort()
    if verbose:
        print('feature_names :',feature_names)
    # Create a mask to filter the DataFrame
    mask = pd.Series(
        data  = True,
        index = df_features_filtre.index,
    )
    # Loop over the features of the rule S
    for feature_name in feature_names:
        if verbose:
            print('• feature_name :',feature_name)
        # Take the value of the feature in the rule S
        feature_S = S[feature_name]
        if verbose:
            print('•- feature_S :',feature_S)
        # Take the btype of the feature
        if feature_name in solver.columns_types.keys():
            # If the type is specified in the solver, we take it
            feature_type = solver.columns_types[feature_name]
        else:
            # If the type is not specified in the solver, we guess it from the rule
            if isinstance(S[feature_name],list):
                feature_type = 'continuous'
            else:
                feature_type = 'multiclass'
        if verbose:
            print('•- feature_type :',feature_type)
        """
        The types :

        - binary
        - multiclass
        - continuous
        - ignore
        """
        # Depending on the type of the feature the data is filtered differently
        if feature_type=='ignore':
            # If the variable has the type 'ignore', we skip it.
            continue
        elif feature_type in ['binary','multiclass']:
            # If the variable is a categorical variable
            if feature_S==set():
                # If the variable can take no modality, return an empty list
                return pd.Index([],name=df_features_filtre.index.name)
            if isinstance(feature_S,int):
                # If the rule is an integer, convert to a set with one element
                feature_S = {feature_S}
            elif isinstance(feature_S,float):
                # If the rule is a float, convert to a set with one element
                if pd.isna(feature_S):
                    # If the float is a NaN, convert it to 'nan'
                    feature_S = 'nan'
                elif int(feature_S)==feature_S:
                    # If the float is an integer, convert it to an integer (to have 0 or 1 instead of 0.0 or 1.0)
                    feature_S = int(feature_S)
                # Convert to a set with one element
                feature_S = {feature_S}
            elif isinstance(feature_S,str):
                # If the rule is a string, convert to a set with one element
                feature_S = {feature_S}
            if verbose:
                print('•- feature_S :',feature_S)
            # Create a temporary mask to filter the DataFrame
            mask_temp = pd.Series(
                data  = False,
                index = df_features_filtre.index,
            )
            # Loop over the modalities of the rule S
            for modality in feature_S:
                if modality in [np.nan,'nan']:
                    # If the modality is NaN
                    # Keep the NaNs
                    mask_temp |= df_features_filtre[feature_name].isna()
                elif modality=='other':
                    # If the modality is 'other'
                    if 'other' in df_features_filtre[feature_name].values:
                        # If 'other' is a modality of the original data
                        # Keep the modality 'other'
                        mask_temp |= (df_features_filtre[feature_name]=='other')
                    if feature_name in solver.other_modalities.keys():
                        # If the feature is present in the conversion to other modalities
                        if len(solver.other_modalities[feature_name])>0:
                            # If at least one modality was mapped to 'other'
                            # Take the other modalities
                            other_modalities = solver.other_modalities[feature_name]
                            # Keep the other modalities
                            mask_temp |= (df_features_filtre[feature_name].isin(other_modalities))
                elif modality in df_features_filtre[feature_name].values:
                    # If the modality is in the original data
                    # Keep the modality
                    mask_temp |= (df_features_filtre[feature_name]==modality)
                elif str(modality) in df_features_filtre[feature_name].values:
                    # If str(modality) is in the original data
                    # Keep str(modality)
                    print("WARNING: 'str(modality)' is in the data but not 'modality'.")
                    mask_temp |= (df_features_filtre[feature_name]==str(modality))
                else:
                    if all_modalities_should_be_present:
                        raise Exception(f"ERROR: the modality='{modality}' is not in the data.")                        
        elif feature_type=='continuous':
            # If the feature is continuous
            if isinstance(feature_S[0],list):
                # If the feature is continuous with NaNs
                [[s_rule_min,s_rule_max],include_or_exlude_nan] = feature_S
                if verbose:
                    print('•- s_rule_min =',s_rule_min)
                    print('•- s_rule_max =',s_rule_max)
                    print('•- include_or_exlude_nan =',include_or_exlude_nan)
                # Take the continuous values of the feature
                s = df_features_filtre[feature_name]
                # Keep only the values between the interval
                mask_temp = (s_rule_min<=s)&(s<=s_rule_max)
                # Handle NaNs
                if include_or_exlude_nan=='exclude_nan':
                    # NaNs are a priori excluded because (s_rule_min<=s)&(s<=s_rule_max) can only be True for non NaNs.
                    ...
                elif include_or_exlude_nan=='include_nan':
                    # If we want to include NaNs
                    mask_temp |= s.isna()
                else:
                    raise Exception(f"ERROR: include_or_exlude_nan='{include_or_exlude_nan}' should be either 'include_nan' or 'exclude_nan'.")
            else:
                # If the feature is continuous without NaNs
                s_rule_min,s_rule_max = feature_S
                if verbose:
                    print('•- s_rule_min =',s_rule_min)
                    print('•- s_rule_max =',s_rule_max)
                # Take the continuous values of the feature
                s = df_features_filtre[feature_name]
                # Keep only the values between the interval
                mask_temp = (s_rule_min<=s)&(s<=s_rule_max)
        mask &= mask_temp
        if verbose:
            print("•- Number of points remaining:",mask.sum())
    # Filter the data
    df_features_filtre = df_features_filtre[mask]
    # Take the index
    index = df_features_filtre.index
    # Sort the index
    index = index.sort_values()
    # Return the index
    return index

def resolve_language(
    language: str         = 'auto',
    default_language: str = 'english',
)->str:
    # Make sure the string is not too long (otherwise it's suspicious)
    if len(language)>100:
        raise Exception(f"ERROR (resolve_language): invalid llm language because it has more than 100 characters: '{resolve_language}'.")
    # Handle the default option
    if language=='auto':
        language = default_language
    # Handle various options
    if language=='fr':
        language = 'français'
    elif language=='en':
        language = 'anglais'
    elif language=='french':
        language = 'français'
    elif language=='english':
        language = 'anglais'
    # Make sure the language is valid
    valid_languages = [
        'français',
        'anglais',
    ]
    if language not in valid_languages:
        raise Exception(f"ERROR (resolve_language): invalid llm language='{language}', it must be in {valid_languages}.")
    # Return the result
    return language

def gain_to_percent(
    gain: float,
    decimals: int = 2,
)->str:
    """
    This function formats the gain to either a positive percentage or a negative percentage.

    Parameters
    ----------
    gain: float
        The gain (gain = lift - 1).
    decimals: int
        Number of decimals to show.
    """
    if gain>=0:
        return f"+{round(100*gain,decimals)}%"
    else:
        return f"{round(100*gain,decimals)}%"


################################################################################
################################################################################
# Defining the API Client

def search_best_ruleset_from_API_public(
    df                      : pd.DataFrame,                                        # The Pandas DataFrame that contains the data to analyse.
    computing_source        : str                                        = 'auto', # Specify if the execution is local or remote
    input_file_service_key  : Optional[str]                              = None,   # For a remote execution from outside GCP, a service key file is necessary
    user_email              : Optional[str]                              = None,   # For a remote execution from inside GCP, a user email is necessary
    target_name             : Optional[Union[str,int]]                   = None,   # Name of the target variable
    target_goal             : Optional[Union[str,numbers.Real,np.uint8]] = None,   # Target goal
    columns_names_to_btypes : Optional[Dict]                             = dict(), # Specify the btypes of the variables
    columns_names_to_descr  : Optional[Dict]                             = dict(), # Specify the descriptions of the variables
    threshold_M_max         : Optional[int]                              = None,   # Specify the maximum number of rows to use in the rule mining
    specified_constraints   : Optional[Dict]                             = dict(), # Specify some constraints on the rules
    top_N_rules             : Optional[int]                              = 10,     # Maximum number of rules to keep
    verbose                 : bool                                       = False,  # Verbosity
    filtering_score         : str                                        = 'auto', # Filtering score
    api_source              : str                                        = 'auto', # Source of the API call
    do_compress_data        : bool                                       = True,   # If we want to compress the communications (slower to compress but faster to transmit)
    do_compute_memory_usage : bool                                       = True,   # If we want to compute the memory usage of the API (this significantly slows down computation time but is good for monitoring purposes)
    n_benchmark_original    : int                                        = 5,      # Number of benchmarking runs to execute where the target is not shuffled.
    n_benchmark_shuffle     : int                                        = 20,     # Number of benchmarking runs to execute where the target is shuffled.
    do_llm_readable_rules   : bool                                       = False,  # If we want to convert the rules to a readable format using a LLM.
    llm_source              : str                                        = 'remote_gemini', # Source where the LLM is running.
    llm_language            : str                                        = 'auto', # Language of the LLM.
    do_store_llm_cache      : bool                                       = True,   # If we want to store the result of the LLM in the cache (makes futur LLM calls faster).
    do_check_llm_cache      : bool                                       = True,   # If we want to check if the results of the prompt are found in the cache (makes LLM calls faster).
)->dict:
    """
    This function is meant to make a rule mining API call.

    Parameters
    ----------
    df: DataFrame
        The DataFrame that contains the data to analyse (a target column and various feature columns).
    computing_source: str
        If the rule mining should be computed locally or remotely.
    input_file_service_key: str
        The string that specifies the path to the service key (necessary to use the remote Cloud Function from outside GCP).
    user_email: str
        The email of the user (necessary to use the remote Cloud Function from inside GCP).
    target_name: str
        Name of the column of the target variable.
    target_goal: str (or other modality of the target variable)
        Target goal.
    columns_names_to_btypes: dict
        A dict that specifies the btypes of the columns.
    columns_names_to_descr: dict
        A dict that specifies the descriptions of the columns.
    threshold_M_max: int
        Threshold on the maximum number of points to use during the rule mining (max. 40000 pts in the public API).
    specified_constraints: dict
        A dict that specifies contraints to be used during the rule mining.
    top_N_rules: int
        An integer that specifies the maximum number of rules to get from the rule mining.
    verbose: bool
        Verbosity.
    filtering_score: str
        A string that specifies the filtering score to be used when selecting rules.
    api_source: str
        A string used to identify the source of the API call.
    do_compress_data: bool
        A boolean that specifies if we want to compress the data.
    do_compute_memory_usage: bool
        A bool that specifies if we want to get the memory usage of the computation.
    n_benchmark_original: int
        Number of benchmarking runs to execute where the target is not shuffled.
    n_benchmark_shuffle: int
        Number of benchmarking runs to execute where the target is shuffled.
    do_llm_readable_rules: bool
        If we want to convert the rules to a readable format using a LLM.
    llm_source: str
        Source where the LLM is running
    do_store_llm_cache: bool
        If we want to store the result of the LLM in the cache (makes futur LLM calls faster).
    do_check_llm_cache: bool
        If we want to check if the results of the prompt are found in the cache (makes LLM calls faster).

    Returns
    -------
    response: requests.models.Response
        A response object obtained from the API call that contains the rule mining results.
    """
    # Manage where the computation is executed
    if computing_source=='auto':
        computing_source='remote_cloud_function'
    # If the computation is in a local server, the local server will not have the service key and so will not use the remote LLM
    if do_llm_readable_rules&(computing_source=='local_cloud_function'):
        if verbose:
            print("WARNING (search_best_ruleset_from_API_public): do_llm_readable_rules is True but the computing source is a local server, so do_llm_readable_rules is set to False.")
        do_llm_readable_rules = False
    # Taking the global variables
    if api_source=='auto':
        api_source = API_SOURCE_PUBLIC
    # Manage the btypes
    if columns_names_to_btypes==None:
        columns_names_to_btypes = dict()
    # Manage the specified constraints
    if specified_constraints==None:
        specified_constraints = dict()
    # Manage top_N_rules
    if top_N_rules==None:
        top_N_rules = 10
    # Convert the Pandas DataFrame to JSON
    df_to_dict = df.to_json()
    # Create a dict that contains relevant informations for rule mining
    d_out_original = {
        'df_to_dict'              : df_to_dict,
        'target_name'             : target_name,
        'target_goal'             : target_goal,
        'columns_names_to_btypes' : columns_names_to_btypes,
        'columns_names_to_descr'  : columns_names_to_descr,
        'threshold_M_max'         : threshold_M_max,
        'specified_constraints'   : specified_constraints,
        'top_N_rules'             : top_N_rules,
        'filtering_score'         : filtering_score,
        'api_source'              : api_source,
        'n_benchmark_original'    : n_benchmark_original,
        'n_benchmark_shuffle'     : n_benchmark_shuffle,
        'do_llm_readable_rules'   : do_llm_readable_rules,
        'llm_source'              : llm_source,
        'llm_language'            : llm_language,
        'do_store_llm_cache'      : do_store_llm_cache,
        'do_check_llm_cache'      : do_check_llm_cache,
    }
    # Make the API call
    from .api_utilities import search_best_ruleset_from_API_dict
    d_in_original = search_best_ruleset_from_API_dict(
        d_out_original          = d_out_original,
        input_file_service_key  = input_file_service_key,
        user_email              = user_email,
        computing_source        = computing_source,
        do_compress_data        = do_compress_data,
        do_compute_memory_usage = do_compute_memory_usage,
        verbose                 = verbose,
    )
    # Return the result
    return d_in_original

################################################################################
################################################################################
# Credits

def get_credits_available(
    computing_source:str      = 'auto', # Where to compute the rule mining
    service_key:Optional[str] = None,   # Path+name of the service key
    user_email:Optional[str]  = None,   # User email
):
    """
    This function is meant to retrieve from the server the amount of credits available.
    """
    # Manage where the computation is executed
    if computing_source=='auto':
        computing_source='remote_cloud_function'
    # Create the outgoing dict
    d_out_credits_infos = {
        'do_compute_credits_available' : True,
        'do_compute_df_credits_infos'  : False,
    }
    # Send the dict to the API server and receive a new dict
    from .api_utilities import request_cloud_credits_infos
    d_in_credits_infos = request_cloud_credits_infos(
        computing_source       = computing_source,
        d_out_credits_infos    = d_out_credits_infos,
        input_file_service_key = service_key,
        user_email             = user_email,
    )
    # Extract the credits available
    credits_available = d_in_credits_infos['credits_available']
    # Return the result
    return credits_available

################################################################################
################################################################################
# Defining the InsightSolver class

class InsightSolver(Mapping):
    """
    The class ``InsightSolver`` is meant to :

    1. Take input data.
    2. Make an insightsolver API calls to the server.
    3. Present the results of the rule mining.

    Attributes
    ----------
    df: DataFrame
        The DataFrame that contains the data to analyse.
    target_name: str (default None)
        Name of the target variable (by default it's the first column).
    target_goal: (str or int)
        Target goal.
    target_threshold: (int or float)
        Threshold used to convert a continuous target variable to a binary target variable.
    M: int
        Number of points in the population.
    M0: int
        Number of points 0 in the population.
    M1: int
        Number of points 1 in the population.
    columns_types: dict
        Types of the columns.
    columns_descr: dict
        Textual descriptions of the columns.
    other_modalities: dict
        Modalities that are mapped to the modality 'other'.
    threshold_M_max: int (default 40000)
        Threshold on the maximum number of observations to consider, above which we under sample the observations.
    specified_constraints: dict
        Dictionary of the specified constraints on ``m_min``, ``m_max``, ``coverage_min``, ``coverage_max``.
    top_N_rules: int (default 10)
        An integer that specifies the maximum number of rules to get from the rule mining.
    filtering_score: str (default 'auto')
        A string that specifies the filtering score to be used when selecting rules.
    n_benchmark_original: int (default 5)
        An integer that specifies the number of benchmarking runs to execute where the target is not shuffled.
    n_benchmark_shuffle: int (default 20)
        An integer that specifies the number of benchmarking runs to execute where the target is shuffled.
    monitoring_metadata: dict
        Dictionary of monitoring metadata.
    benchmark_scores: dict
        Dictionary of the benchmarking scores against shuffled data.
    rule_mining_results: dict
        Dictionary that contains the results of the rule mining.
    _is_fitted: bool
        Boolean that tells if the solver is fitted.

    Methods
    -------
    __init__: None
        Initialization of an instance of the class InsightSolver.
    __str__: None
        Converts the solver to a string as provided by the print method.
    ingest_dict: None
        Ingests a Python dict.
    ingest_json_string: None
        Ingests a JSON string.
    is_fitted: Bool
        Returns a boolean that tells if the solver is fitted.
    fit: None
        Fits the solver.
    S_to_index_points_in_rule: Pandas Index
        Returns the index of the points in a rule S.
    S_to_s_points_in_rule: Pandas Series
        Returns a boolean Pandas Series that tells if the point is in the rule S.
    S_to_df_filtered: Pandas DataFrame
        Returns the filtered df of rows that are in the rule S.
    ruleset_count: int
        Counts the number of rules held by the InsightSolver.
    i_to_rule: dict
        Gives the rule i of the InsightSolver.
    i_to_S: dict
        Returns the rule S for the rule at index i.
    i_to_subrules_dataframe: Pandas DataFrame
        Returns a DataFrame containing the informations about the subrules of the rule i.
    i_to_feature_contributions_S: Pandas DataFrame
        Returns a DataFrame of the feature contributions of the variables in the rule S at position i.
    i_to_readable_text: str
        Returns the readable text of the rule i if it is available.
    i_to_print: None
        Prints the content of the rule i in the InsightSolver.
    get_range_i: list
        Gives the range of i in the InsightSolver.
    print: None
        Prints the content of the InsightSolver.
    print_light: None
        Prints the content of the InsightSolver ('light' mode).
    print_dense: None
        Prints the content of the InsightSolver ('dense' mode).
    to_dict: dict
        Exports the content of the InsightSolver object to a Python dict.
    to_json_string: str
        Exports the content of the InsightSolver object to a JSON string.
    to_dataframe: Pandas DataFrame
        Exports the rule mining results to a Pandas DataFrame.
    to_csv: str
        Exports the rule mining results to a CSV string and/or a local CSV file.
    to_excel: None
        Exports the rule mining results to a Excel file.
    to_excel_string: str
        Exports the rule mining results to a Excel string.
    get_credits_needed_for_computation: int
        Get the number of credits needed for the fitting computation of the solver.
    get_df_credits_infos: Pandas DataFrame
        Get a DataFrame of the transactions involving credits.
    get_credits_available: int
        Get the number of credits available.
    convert_target_to_binary: pd.Series
        Converts the target variable to a binary {0,1}-valued Pandas Series.
    compute_mutual_information: pd.Series
        Computes a Pandas Series of the mutual information between features and the target variable.
    to_pdf: str
         Generates a PDF containing all visualization figures for the solver.
    to_zip: str
        Exports the rule mining results to a ZIP file.

    Example
    -------
    Here's a sample code to use the class ``InsightSolver``::

        # Specify the service key
        service_key = 'name_of_your_service_key.json'
        
        # Import some data
        import pandas as pd
        df = pd.read_csv('kaggle_titanic_train.csv')
        
        # Specify the name of the target variable
        target_name = 'Survived' # We are interested in whether the passengers survived or not
        
        # Specify the target goal
        target_goal = 1 # We are searching rules that describe survivors
        
        # Import the class InsightSolver from the module insightsolver
        from insightsolver import InsightSolver
        
        # Create an instance of the class InsightSolver
        solver = InsightSolver(
            df          = df,          # A dataset
            target_name = target_name, # Name of the target variable
            target_goal = target_goal, # Target goal
        )
        
        # Fit the solver
        solver.fit(
            service_key = service_key, # Use your API service key here
        )
        
        # Print the rule mining results
        solver.print()
    """

    def __init__(
        self,
        verbose: bool                                           = False,  # Verbosity during the initialization of the solver
        df: pd.DataFrame                                        = None,   # DataFrame that contains the data from which we wish to extract insights
        target_name: Optional[Union[str,int]]                   = None,   # Name of the target variable
        target_goal: Optional[Union[str,numbers.Real,np.uint8]] = None,   # Target goal
        columns_types: Optional[Dict]                           = dict(), # Types of the columns
        columns_descr:Optional[Dict]                            = dict(), # Descriptions of the columns
        threshold_M_max: Optional[int]                          = 40000,  # Maximum number of observations to consider (by default 40000)
        specified_constraints: Optional[Dict]                   = dict(), # Specified constraints on the rule mining
        top_N_rules: Optional[int]                              = 10,     # Maximum number of rules to get from the rule mining
        filtering_score: str                                    = 'auto', # Filtering score to be used when selecting rules.
        n_benchmark_original: int                               = 5,      # Number of benchmarking runs to execute without shuffling.
        n_benchmark_shuffle: int                                = 20,     # Number of benchmarking runs to execute with shuffling.
    ):
        """
        The initialization occurs when an ``InsightSolver`` class instance is created.

        Parameters
        ----------
        verbose: bool (default False)
            If we want the initialization to be verbose.
        df: DataFrame
            The DataFrame that contains the data to analyse (a target column and various feature columns).
        target_name: str
            Name of the column of the target variable.
        target_goal: str (or other modality of the target variable)
            Target goal.
        columns_types: dict
            Types of the columns.
        columns_descr: dict
            Descriptions of the columns.
        threshold_M_max: int
            Threshold on the maximum number of observations to consider, above which we sample observations.
        specified_constraints: dict
            Dictionary of the specified constraints on m_min, m_max, coverage_min, coverage_max.
        top_N_rules: int (default 10)
            An integer that specifies the maximum number of rules to get from the rule mining.
        filtering_score: str (default 'auto')
            A string that specifies the filtering score to be used when selecting rules.
        n_benchmark_original: int (default 5)
            An integer that specifies the number of benchmarking runs to execute where the target is not shuffled.
        n_benchmark_shuffle: int (default 20)
            An integer that specifies the number of benchmarking runs to execute where the target is shuffled.
        
        Returns
        -------
        solver: InsightSolver
            An instance of the class InsightSolver.

        Example
        -------
        Here's a sample code to instantiante the class ``InsightSolver``::

            # Import the class InsightSolver from the module insightsolver
            from insightsolver import InsightSolver

            # Create an instance of the class InsightSolver
            solver = InsightSolver(
                df          = df,          # A Pandas DataFrame
                target_name = target_name, # Name of the target variable
                target_goal = target_goal, # Target goal
            )
        """
        if verbose:
            print('Initializing an instance of the class InsightSolver...')
        # Validate the integrity of the class
        columns_types = validate_class_integrity(
            df                    = df,
            target_name           = target_name,
            target_goal           = target_goal,
            columns_types         = columns_types,
            columns_descr         = columns_descr,
            threshold_M_max       = threshold_M_max,
            specified_constraints = specified_constraints,
            top_N_rules           = top_N_rules,
            filtering_score       = filtering_score,
            n_benchmark_original  = n_benchmark_original,
            n_benchmark_shuffle   = n_benchmark_shuffle,
            do_strict_types       = False,
            verbose               = verbose,
        )
        # Handling threshold_M_max
        if threshold_M_max==None:
            threshold_M_max = 40000 # If the limit is set to None, we send at most 40000 rows to the server.
        elif threshold_M_max>40000:
            threshold_M_max = 40000 # The server will only accept at most 40000 rows.
        self.threshold_M_max = threshold_M_max
        # Sample df
        if len(df)>self.threshold_M_max:
            # Sample df locally to limit the amount of data sent to the server.
            self.df = df.sample(
                n            = self.threshold_M_max,
                random_state = 0,
            )
        else:
            # No need to sample the data
            self.df = df.copy()
        # Execution metadata
        self.target_name             = target_name
        self.target_goal             = target_goal
        self.target_threshold        = None
        self.M                       = None
        self.M0                      = None
        self.M1                      = None
        self.columns_types           = columns_types
        self.columns_descr           = columns_descr
        self.other_modalities        = None
        self.specified_constraints   = specified_constraints
        self.top_N_rules             = top_N_rules
        self.filtering_score         = filtering_score
        self.n_benchmark_original    = n_benchmark_original
        self.n_benchmark_shuffle     = n_benchmark_shuffle
        # Monitoring metadata
        self.monitoring_metadata     = dict()
        # Benchmarking scores
        self.benchmark_scores        = dict()
        # Rule mining results
        self.rule_mining_results     = dict()
        # Boolean that tells if the solver is fitted
        self._is_fitted              = False
    def __str__(
        self,
    )->str:
        """
        This method can convert a solver object to a string via str(solver).
        This lets print(solver) return solver.print().
        """
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.print()
        return buf.getvalue().strip()
    def __getitem__(
        self,
        key,
    ):
        """
        This method makes the solver behave like a dict:

        ``
        for i in solver: rule = solver[i]
        ``
        """
        return self.rule_mining_results[key]
    def __iter__(
        self,
    ):
        """
        This method makes the solver an iterable.
        A loop on it will loop over keys of the dict rule_mining_results.

        For example: ``for i in solver: ...``.
        """
        return iter(self.rule_mining_results)
    def __len__(
        self,
    )->int:
        """
        This method lets len(solver) returns the number of rules in the solver.
        """
        return self.ruleset_count()
    def ingest_dict(
        self,
        d: dict,               # The dict to ingest
        verbose: bool = False, # The verbosity
    )->None:
        """
        This method aims to ingest a Python dict in the solver.
        """
        # dataset_metadata
        if verbose:
            print('Reading dataset_metadata...')
        if 'dataset_metadata' in d:
            if 'target_threshold' in d['dataset_metadata']:
                self.target_threshold = d['dataset_metadata']['target_threshold']
            else:
                self.target_threshold = None
            if 'M' in d['dataset_metadata']:
                self.M  = d['dataset_metadata']['M']
            else:
                self.M = None
            if 'M0' in d['dataset_metadata']:
                self.M0 = d['dataset_metadata']['M0']
            else:
                self.M0 = None
            if 'M1' in d['dataset_metadata']:
                self.M1 = d['dataset_metadata']['M1']
            else:
                self.M1 = None
            if 'columns_names_to_descr' in d['dataset_metadata']:
                self.columns_descr = d['dataset_metadata']['columns_names_to_descr']
            else:
                self.columns_descr = None
            if 'columns_names_to_btypes' in d['dataset_metadata']:
                for column_name,column_btype in d['dataset_metadata']['columns_names_to_btypes'].items():
                    if (column_name in self.columns_types) and (self.columns_types[column_name]!=column_btype):
                        if column_name==self.target_name:
                            # The server will convert a continuous target to a binary target so we ignore this change.
                            continue
                        else:
                            print(f"WARNING: for column_name='{column_name}', the btype in the solver is '{self.columns_types[column_name]}' but it does not match the btype='{column_btype}' coming from the server. The btype in the solver is overwritten by the btype coming from the server.")
                    self.columns_types[column_name] = column_btype
            if 'features_names_to_other_modalities' in d['dataset_metadata']:
                self.other_modalities = d['dataset_metadata']['features_names_to_other_modalities']
            else:
                self.other_modalities = None
        else:
            print("WARNING : dict does not have key 'dataset_metadata'.")
            self.M                = None
            self.M0               = None
            self.M1               = None
            self.other_modalities = None
        # monitoring_metadata
        if verbose:
            print('Reading monitoring_metadata...')
        if 'monitoring_metadata' in d:
            self.monitoring_metadata = d['monitoring_metadata'].copy()
        else:
            print("WARNING : dict does not have key 'monitoring_metadata'.")
            self.monitoring_metadata = dict()
        # benchmark_scores
        if verbose:
            print('Reading benchmark_scores...')
        if 'benchmark_scores' in d:
            self.benchmark_scores = d['benchmark_scores'].copy()
        else:
            print("WARNING : dict does not have key 'benchmark_scores'.")
            self.benchmark_scores = dict()
        # rule_mining_results
        if verbose:
            print('Reading rule_mining_results...')
        if 'rule_mining_results' in d:
            self.rule_mining_results = d['rule_mining_results']
        else:
            print("WARNING : dict does not have key 'rule_mining_results'.")
            self.rule_mining_results = dict()
    def ingest_json_string(
        self,
        json_string: str,      # JSON string to ingest
        verbose: bool = False, # Verbosity
    )->None:
        """
        This method aims to ingest a JSON string in the solver.
        """
        # Convert the json_string to a dict
        from .api_utilities import convert_json_string_to_dict
        d = convert_json_string_to_dict(json_string)
        self.ingest_dict(d)
        # The keys of the rules are given as string, we need to convert them to integers
        self.rule_mining_results = {int(k):self.rule_mining_results[k] for k in self.rule_mining_results.keys()}
    def is_fitted(
        self,
    ):
        """
        This method returns a boolean that tells if the solver is fitted.
        """
        return self._is_fitted
    def fit(
        self,
        verbose:bool                 = False,  # Verbosity
        computing_source:str         = 'auto', # Where to compute the rule mining
        service_key:Optional[str]    = None,   # Path+name of the service key
        user_email:Optional[str]     = None,   # User email
        api_source:str               = 'auto', # Source of the API call
        do_compress_data:bool        = True,   # If we want to compress the data for the communications with the server
        do_compute_memory_usage:bool = True,   # If we want to monitor the first thread memory usage on the server side
        do_check_enough_credits:bool = False,  # Check if there are enough credits to fit the solver
        do_llm_readable_rules: bool  = True,   # If we want to convert the rules to a readable format using a LLM.
        llm_source: str              = 'auto', # Source where the LLM is running.
        llm_language: str            = 'auto', # Language of the LLM.
        do_store_llm_cache: bool     = True,   # If we want to store the result of the LLM in the cache (makes futur LLM calls faster).
        do_check_llm_cache: bool     = True,   # If we want to check if the results of the prompt are found in the cache (makes LLM calls faster).
    )->None:
        """
        This method aims to fit the solver.

        Parameters
        ----------
        verbose: bool (default False)
            If we want the fitting to be verbose.
        computing_source: str (default 'auto')
            Specify where the rule mining computation is done ('local_cloud_function' or 'remote_cloud_function').
        service_key: str (default None)
            Path+name of the service key.
        user_email: str (default None)
            User email.
        api_source: str (default 'auto')
            Source of the API call.
        do_compress_data: bool (default True)
            If we want to compress the data for the communications with the server.
        do_compute_memory_usage: bool (default True)
            If we want to monitor the first thread memory usage on the server side.
        do_check_enough_credits: bool (default False)
            Check if there are enough credits to fit the solver.
        do_llm_readable_rules: bool (default True)
            If we want to convert the rules to a readable format using a LLM.
        llm_source: str (default 'auto')
            Source where the LLM is running.
        llm_language: str (default 'auto')
            Language of the LLM.
        do_store_llm_cache: bool (default True)
            If we want to store the result of the LLM in the cache (makes futur LLM calls faster).
        do_check_llm_cache: bool (default True)
            If we want to check if the results of the prompt are found in the cache (makes LLM calls faster).
        """
        if verbose:
            print('Fitting the InsightSolver...')
        # Taking the global variables
        if api_source=='auto':
            api_source = API_SOURCE_PUBLIC
        # Resolve the language
        llm_language = resolve_language(
            language         = llm_language,
        )
        # Check if there are enough credits to fit the solver
        if do_check_enough_credits:
            if computing_source!='local_cloud_function':
                # Get the number of credits needed
                credits_needed = self.get_credits_needed_for_computation()
                # Get the number of credits available
                credits_available = self.get_credits_available(
                    computing_source = computing_source,
                    service_key      = service_key,
                    user_email       = user_email,
                )
                # If the available credits are below the needed credits, raise an exception
                if credits_needed>credits_available:
                    raise Exception(f"ERROR: There is only {credits_available} credits available but {credits_needed} credits are needed.")

        # Make a rule mining API call
        d_in_original = search_best_ruleset_from_API_public(
            df                      = self.df,
            computing_source        = computing_source,
            input_file_service_key  = service_key,
            user_email              = user_email,
            target_name             = self.target_name,
            target_goal             = self.target_goal,
            columns_names_to_btypes = self.columns_types,
            columns_names_to_descr  = self.columns_descr,
            threshold_M_max         = self.threshold_M_max,
            specified_constraints   = self.specified_constraints,
            top_N_rules             = self.top_N_rules,
            n_benchmark_original    = self.n_benchmark_original,
            n_benchmark_shuffle     = self.n_benchmark_shuffle,
            verbose                 = verbose,
            filtering_score         = self.filtering_score,
            api_source              = api_source,
            do_compress_data        = do_compress_data,
            do_compute_memory_usage = do_compute_memory_usage,
            do_llm_readable_rules   = do_llm_readable_rules,
            llm_source              = llm_source,
            llm_language            = llm_language,
            do_store_llm_cache      = do_store_llm_cache,
            do_check_llm_cache      = do_check_llm_cache,
        )
        # Ingest the untransformed incoming dict
        self.ingest_dict(
            d = d_in_original,
        )
        # Set the solver as fitted
        self._is_fitted = True
    def S_to_index_points_in_rule(
        self,
        S: dict,
        verbose: bool              = False,
        df: Optional[pd.DataFrame] = None,
    )->pd.Index:
        """
        This method returns the index of the points inside a rule ``S``.
        """
        # Convert the rule S to an index
        index_points_in_rule = S_to_index_points_in_rule(
            solver  = self,
            S       = S,
            verbose = verbose,
            df      = df,
        )
        # Return the index
        return index_points_in_rule
    def S_to_s_points_in_rule(
        self,
        S:dict,
        verbose:bool              = False,
        df:Optional[pd.DataFrame] = None,
    )->pd.Series:
        """
        This method returns a boolean Series that tells if the points are in the rule ``S`` or not.
        """
        # Take a look at if df is provided
        if not isinstance(df,pd.DataFrame):
            # If df is not provided we take the one in the solver
            df = self.df
        # Make sure that df is a DataFrame
        if not isinstance(df,pd.DataFrame):
            raise Exception(f"ERROR: df must be a DataFrame but not '{type(df)}'.") 
        # Take the index of the points in the rule S
        index_points_in_rule = self.S_to_index_points_in_rule(
            S       = S,
            verbose = verbose,
            df      = df,
        )
        # Create a Pandas Series that tells if the points are in the rule or not
        s_points_in_rule = pd.Series(
            data  = False,
            index = df.index,
            name  = 'in_S',
            dtype = bool,
        )
        s_points_in_rule.loc[index_points_in_rule] = True
        # Return the result
        return s_points_in_rule
    def S_to_df_filtered(
        self,
        S:dict,
        verbose:bool              = False,
        df:Optional[pd.DataFrame] = None,
    ):
        """
        This method returns the DataFrame of rows of ``df`` that lie inside a rule ``S``.
        """
        # Take a look at if df is provided
        if not isinstance(df,pd.DataFrame):
            # If df is not provided we take the one in the solver
            df = self.df
        # Take the index of the points in the rule S
        index_points_in_rule = self.S_to_index_points_in_rule(
            S       = S,
            verbose = verbose,
            df      = df,
        )
        # Create a copy of the DataFrame of the filtered rows
        df_filtered = df.loc[index_points_in_rule].copy()
        # Return the result
        return df_filtered
    def ruleset_count(
        self,
    )->int:
        """
        This method returns the number of rules held in an instance of the solver.
        """
        return len(self.rule_mining_results)
    def i_to_rule(
        self,
        i:int, # Key i of the rule
    )->dict:
        rule_i = self.rule_mining_results[i]
        return rule_i
    def i_to_S(
        self,
        i,
    ):
        """
        This method returns the rule ``S`` at position ``i``.
        """
        # Take the rule at position i
        rule_i = self.i_to_rule(i=i)
        # Take the rule S at position i
        rule_S = rule_i['rule_S']
        # Return the result
        return rule_S
    def i_to_subrules_dataframe(
        self,
        i:int = 0,  # Number of the rule in the InsightSolver
    )->pd.DataFrame:
        """
        This method returns a DataFrame which contains the informations about the subrules of the rule ``i``.
        """

        # Take the rule at position i
        rule_i = self.i_to_rule(i=i)

        # Take the subrules
        subrules_S = rule_i['subrules_S']

        # Convert it to a DataFrame
        if len(subrules_S)>0:
            df_subrules_S = pd.DataFrame.from_dict(
                data   = rule_i['subrules_S'],
                orient = 'columns',
            )
        else:
            print('WARNING: The incoming rule is trivial. An empty DataFrame will be returned.')
            cols = [
                'p_value',
                'Z_score',
                'F_score',
                'M',
                'M0',
                'M1',
                'm',
                'm0',
                'm1',
                'coverage',
                'm1/M1',
                'mu_rule',
                'mu_pop',
                'sigma_pop',
                'F1_pop',
                'lift',
                'gain',
                'complexity',
                'subrule_S',
                'var_name',
                'var_rule',
                'p_value_ratio',
                'mc',
                'm0c',
                'm1c',
                'G_bad_class',
                'G_information',
                'G_gini',
                'KL_divergence',
            ]
            df_subrules_S = pd.DataFrame(columns=cols)

        # Rename some columns
        d_rename = {
            'var_name' : 'variable',
            'var_rule' : 'rule',
            'm1/M1'    : 'TPR', # Sensitivity = coverage of the 1
            'mu_rule'  : 'PPV', # Precision   = purity
        }
        df_subrules_S.rename(columns=d_rename,inplace=True)

        # Parse the shuffling_scores if they are there
        if ('shuffling_scores' in df_subrules_S.columns)&(len(df_subrules_S)>0):
            if 'p_value' in df_subrules_S['shuffling_scores'].iloc[0]:
                df_subrules_S['p_value_cohen_d']  = df_subrules_S['shuffling_scores'].apply(lambda x:x['p_value']['cohen_d'])
                df_subrules_S['p_value_wy_ratio'] = df_subrules_S['shuffling_scores'].apply(lambda x:x['p_value']['wy_ratio'])
            if 'Z_score' in df_subrules_S['shuffling_scores'].iloc[0]:
                df_subrules_S['Z_score_cohen_d']  = df_subrules_S['shuffling_scores'].apply(lambda x:x['Z_score']['cohen_d'])
                df_subrules_S['Z_score_wy_ratio'] = df_subrules_S['shuffling_scores'].apply(lambda x:x['Z_score']['wy_ratio'])
            if 'F_score' in df_subrules_S['shuffling_scores'].iloc[0]:
                df_subrules_S['F_score_cohen_d']  = df_subrules_S['shuffling_scores'].apply(lambda x:x['F_score']['cohen_d'])
                df_subrules_S['F_score_wy_ratio'] = df_subrules_S['shuffling_scores'].apply(lambda x:x['F_score']['wy_ratio'])

        # Move some columns left
        first_cols = [
            'p_value_ratio',
            'variable',
            'rule',
            'complexity',
            'p_value',
            'F_score',
            'Z_score',
            'TPR',
            'PPV',
            'coverage',
            'm',
            'm0',
            'm1',
        ]
        df_subrules_S = df_subrules_S[first_cols + [col for col in df_subrules_S.columns if col not in first_cols]]

        # Return the result
        return df_subrules_S
    def i_to_feature_contributions_S(
        self,
        i: int,                            # Key i of the rule
        do_rename_cols: bool       = True, # If we want to rename some columns
        do_ignore_col_rule_S: bool = True, # Of we want to ignore some columns
    )->pd.DataFrame:
        """
        This method returns a DataFrame of the feature contributions of the variables in the rule ``S`` at position ``i``.
        """
        df_feature_contributions_S = pd.DataFrame.from_dict(
            data   = self.i_to_rule(i)['feature_contributions_S'],
            orient = 'columns',
        )
        df_feature_contributions_S.index.name = 'feature_name'
        if len(df_feature_contributions_S)==0:
            print('WARNING: The incoming rule is trivial. An empty DataFrame will be returned.')
        if do_ignore_col_rule_S:
            df_feature_contributions_S.drop(columns='rule_S',inplace=True)
        if do_rename_cols:
            df_feature_contributions_S.columns = [col.replace('_contribution','') for col in df_feature_contributions_S.columns]
        return df_feature_contributions_S
    def i_to_feature_names(
        self,
        i:int,
        do_sort:bool = True,
    ):
        """
        Returns the list of feature names in the rule at position ``i``.
        The feature are sorted by contribution, descending.

        Parameters
        ----------
        i: int
            Index of the rule in the solver.
        do_sort: bool
            If we want to sort the features by contribution, descending.
        """
        # Take the solver
        solver = self
        # Look at if it is fitted
        if not solver._is_fitted:
            # Raise an exception
            raise Exception(f"ERROR (i_to_feature_names): the solver is not fitted yet.")
        elif i>=len(solver):
            raise Exception(f"ERROR (i_to_feature_names): i={i} is out of range for the solver.")
        else:
            # Take the rule S
            S = solver.i_to_S(i=i)
            # Take the feature names
            feature_names = list(S.keys())
            # Sort the features if required
            if do_sort:
                rule_i = solver.i_to_rule(i=i)
                feature_names.sort(key = lambda feature_name:-rule_i['feature_contributions_S']['p_value_contribution'][feature_name])
            # Return the result
            return feature_names
    def i_to_readable_text(
        self,
        i,
    )->Optional[str]:
        """
        Returns the readable text of the rule ``i`` if it is available.
        """
        # Take the rule i
        rule_i = self.i_to_rule(i=i)
        # Try to take the human readable text of the rule
        if 'llm' in rule_i.keys():
            if 'readable' in rule_i['llm']:
                if 'text' in rule_i['llm']['readable']:
                    readable_text = rule_i['llm']['readable']['text']
                else:
                    readable_text = None
            else:
                readable_text = None
        else:
            readable_text = None
        # Return the result
        return readable_text
    def i_to_print(
        self,
        i: int,                                         # Index of the rule to print
        indentation: str                       = '',    # Indentation of some printed elements
        do_print_shuffling_scores: bool        = True,  # If we want to print the shuffling scores
        do_print_rule_DataFrame: bool          = False, # If we want to print a DataFrame of the rule
        do_print_subrules_S: bool              = True,  # If we want to print the DataFrame of subrules
        do_show_coverage_diff: bool            = False, # If we want to show the differences of coverage in the DataFrame of subrules
        do_show_cohen_d: bool                  = True,  # If we want to show the Cohen d in the DataFrame of subrules
        do_show_wy_ratio: bool                 = True,  # If we want to show the WY ratio in the DataFrame of subrules
        do_print_feature_contributions_S: bool = True,  # If we want to print the DataFrame of feature contributions
    )->None:
        """
        This method prints the content of the rule ``i`` in the solver.

        Parameters
        ----------
        i: int
            Index of the rule to print.
        indentation: str
            Indentation of some printed elements.
        do_print_shuffling_scores: bool
            If we want to print the shuffling scores.
        do_print_rule_DataFrame: bool
            If we want to print a DataFrame of the rule.
        do_print_subrules_S: bool
            If we want to print the DataFrame of subrules.
        do_show_coverage_diff: bool
            If we want to show the differences of coverage in the DataFrame of subrules.
        do_show_cohen_d: bool
            If we want to show the Cohen d in the DataFrame of subrules.
        do_show_wy_ratio: bool
            If we want to show the WY ratio in the DataFrame of subrules.
        do_print_feature_contributions_S: bool
            If we want to print the DataFrame of feature contributions.
        """
        # Take the rule i
        rule_i = self.i_to_rule(i=i)
        # Show various scores
        print(f'{indentation}p_value         :',rule_i['p_value'])
        print(f'{indentation}F_score         :',rule_i['F_score'])
        print(f'{indentation}Z_score         :',rule_i['Z_score'])
        print(f'{indentation}M               :',self.M)  # peut être redondant
        print(f'{indentation}M0              :',self.M0) # peut être redondant
        print(f'{indentation}M1              :',self.M1) # peut être redondant
        print(f'{indentation}m               :',rule_i['m'])
        print(f'{indentation}m0              :',rule_i['m0'])
        print(f'{indentation}m1              :',rule_i['m1'])
        print(f'{indentation}m/M (coverage)  :',rule_i['coverage'])
        print(f'{indentation}m1/M1    (TPR)  :',rule_i['m1/M1'])
        print(f'{indentation}μ_rule   (PPV)  :',rule_i['mu_rule'])
        print(f'{indentation}μ_pop           :',rule_i['mu_pop'])    # peut être redondant
        print(f'{indentation}σ_pop           :',rule_i['sigma_pop']) # peut être redondant
        print(f'{indentation}lift            :',rule_i['lift'])
        print(f'{indentation}gain            :',gain_to_percent(gain=rule_i['gain'],decimals=4))
        print(f'{indentation}complexity_S    :',rule_i['complexity_S'])
        print(f'{indentation}F1_pop          :',rule_i['F1_pop'])
        if 'G_bad_class' in rule_i.keys():
            print(f'{indentation}G_bad_class     :',rule_i['G_bad_class'])
        if 'G_information' in rule_i.keys():
            print(f'{indentation}G_information   :',rule_i['G_information'])
        if 'G_gini' in rule_i.keys():
            print(f'{indentation}G_gini          :',rule_i['G_gini'])
        if 'KL_divergence' in rule_i.keys():
            print(f'{indentation}KL_divergence   :',rule_i['KL_divergence'])
        rule_S = rule_i['rule_S']
        print(f'{indentation}rule_S          :',rule_S)
        p_value_ratio_S = {k:v for k,v in rule_i['p_value_ratio_S'].items() if k in rule_i['rule_S'].keys()}
        print(f'{indentation}p_value_ratio_S :',p_value_ratio_S)
        # Show the rule in a human readable textual form if it is available
        readable_text = self.i_to_readable_text(i=i)
        if readable_text:
            print(f'{indentation}text            :',readable_text)
        # Show the shuffling scores
        if do_print_shuffling_scores:
            print('\nShuffling scores :')
            if 'shuffling_scores' in rule_i.keys():
                # Convert the dict of shuffling scores to a Pandas DataFrame
                df_shuffling_scores = pd.DataFrame.from_dict(rule_i['shuffling_scores'], orient='index')
                # Drop the effect_size and the F_score
                df_shuffling_scores.drop(
                    columns = ['effect_size'],
                    index   = ['F_score'],
                    inplace = True,
                )
                # Print the DataFrame
                print(df_shuffling_scores)
            else:
                print("WARNING: 'shuffling_scores' is not in the keys of rule_i.")
        # Show the DataFrame of the rule
        if do_print_rule_DataFrame:
            # Compute the DataFrame of the rule
            df_rules_and_p_value_ratio = pd.concat(
                (
                    pd.Series(rule_S).rename('rule'),
                    pd.Series(p_value_ratio_S).rename('p_value_ratio'),
                ),
                axis=1,
            ).reset_index(
                drop=False,
            ).rename(
                columns={'index':'variable'},
            ).sort_values(
                by='p_value_ratio',
                ascending=True,
            ).reset_index(
                drop=True,
            )
            # Append the complexity
            df_rules_and_p_value_ratio['complexity'] = range(1,len(df_rules_and_p_value_ratio)+1)
            # Show the DataFrame of the rule
            print(f'\nDataFrame of the components and p_value_ratio :')
            print(df_rules_and_p_value_ratio)
        if do_print_subrules_S:
            print('\nDataFrame of the cumulative subrules of S according to the ratio_drop :')
            df_subrules_S = self.i_to_subrules_dataframe(i=i)
            # Select the columns to show
            cols = ['p_value_ratio']
            cols += [
                'variable',
                'rule',
                'complexity',
                'p_value',
                'F_score',
                'Z_score',
                #'G_bad_class',
                'G_information',
                #'G_gini',
                #'KL_divergence',
                'TPR',
                'PPV',
                'lift',
                'gain',
                'coverage',
                'm',
                'm1',
            ]
            if do_show_cohen_d&('Z_score_cohen_d' in df_subrules_S.columns):
                cols += [
                    'cohen_d',
                ]
                df_subrules_S.rename(columns={'Z_score_cohen_d':'cohen_d'},inplace=True)
            if do_show_wy_ratio&('Z_score_wy_ratio' in df_subrules_S.columns):
                cols += [
                    'wy_ratio',
                ]
                df_subrules_S.rename(columns={'Z_score_wy_ratio':'wy_ratio'},inplace=True)
            # If we want to show the difference of the successive coverage of the subrules
            if do_show_coverage_diff:
                df_subrules_S['coverage_diff'] = df_subrules_S['coverage'].diff()
                df_subrules_S.loc[0,'coverage_diff'] = df_subrules_S.loc[0,'coverage']-1
                cols += ['coverage_diff']
            # Keep only certain columns
            df_subrules_S = df_subrules_S[cols]
            # Show the DataFrame
            df_subrules_S_formatted = df_subrules_S.copy()
            do_compactify_print=1
            if do_compactify_print:
                df_subrules_S_formatted['p_value_ratio'] = df_subrules_S_formatted['p_value_ratio'].apply(lambda x:format_value(value=x,format_type='scientific',decimals=4))
                df_subrules_S_formatted['p_value']       = df_subrules_S_formatted['p_value'].map(lambda x:format_value(value=x,format_type='scientific',decimals=4))
                if 'F_score' in df_subrules_S_formatted.columns:
                    df_subrules_S_formatted['F_score']       = df_subrules_S_formatted['F_score'].map('{:.4f}'.format)
                if 'Z_score' in df_subrules_S_formatted.columns:
                    df_subrules_S_formatted['Z_score']       = df_subrules_S_formatted['Z_score'].map('{:.4f}'.format)
                df_subrules_S_formatted['TPR']           = df_subrules_S_formatted['TPR'].map('{:.4f}'.format)
                df_subrules_S_formatted['PPV']           = df_subrules_S_formatted['PPV'].map('{:.4f}'.format)
                df_subrules_S_formatted['lift']          = df_subrules_S_formatted['lift'].map('{:.4f}'.format)
                df_subrules_S_formatted['gain']          = df_subrules_S_formatted['gain'].map(gain_to_percent)
                df_subrules_S_formatted['coverage']      = df_subrules_S_formatted['coverage'].map('{:.4f}'.format)
                if 'cohen_d' in df_subrules_S_formatted.columns:
                    df_subrules_S_formatted['cohen_d'] = df_subrules_S_formatted['cohen_d'].map('{:.4f}'.format)
                if 'wy_ratio' in df_subrules_S_formatted.columns:
                    df_subrules_S_formatted['wy_ratio'] = df_subrules_S_formatted['wy_ratio'].map('{:.4f}'.format)
            d_rename = {
                'complexity':'c',
                #'TPR': 'sensitivity',
                #'PPV': 'purity',
            }
            df_subrules_S_str = df_subrules_S_formatted.rename(
                columns = d_rename,
            ).to_string(
                index = False,
                #float_format = '{:,.4f}'.format
            )
            print(df_subrules_S_str)
        if do_print_feature_contributions_S:
            print('\nDataFrame of the feature contributions of the variables of S :')
            df_feature_contributions_S = self.i_to_feature_contributions_S(
                i              = i,
                do_rename_cols = True,
            )
            print(df_feature_contributions_S)
    def get_range_i(
        self,
        complexity_max: Optional[int] = None,
    )->list:
        """
        This method gives the range of ``i`` in the solver.
        If the integer ``complexity_max`` is specified, return only this number of elements.
        """
        range_i = sorted(self.rule_mining_results.keys())
        if complexity_max:
            if complexity_max<len(range_i):
                range_i = range_i[:complexity_max]
        return range_i
    def print(
        self,
        verbose: bool                                 = False,  # Verbosity
        r: Optional[int]                              = None,   # Number of rules to print. "None" will print all of them. "1" will print only the first one, "2" will print the 1st and 2nd rule, etc.
        do_print_dataset_metadata: bool               = True,   # If we want to print the dataset metadata.
        do_print_monitoring_metadata: bool            = False,  # If we want to print the monitoring metadata.
        do_print_benchmark_scores: bool               = True,   # If we want to print the benchmarking scores.
        do_print_shuffling_scores: bool               = True,   # If we want to print the shuffling scores of the individual rules.
        do_show_cohen_d: bool                         = True,   # If we want to print the d of Cohen of the subrules.
        do_show_wy_ratio: bool                        = True,   # If we want to print the WY ratio of the subrules.
        do_print_rule_mining_results: bool            = True,   # If we want to print the rule mining results.
        do_print_rule_DataFrame: bool                 = False,  # If we want to print the the DataFrame of rules.
        do_print_subrules_S: bool                     = True,   # If we want to print the the DataFrame of the subrules of the rules S.
        do_show_coverage_diff: bool                   = False,  # If we want to show the column 'coverage_diff' of the DataFrame of subrules.
        do_print_feature_contributions_S: bool        = True,   # If we want to show the DataFrame of feature importances of the rules S.
        separation_width_between_rules: Optional[int] = 79,     # If we want to show a line between the different rules.
        do_print_last_separator: bool                 = True,   # If we want to print the last separator.
        mode: str                                     = 'full', # The printing mode.
    )->None:
        """
        This method prints the content of the ``InsightSolver`` solver.
        """
        if verbose:
            print('Printing the content of the class InsightSolver...')
        if mode not in ['full','light','dense']:
            raise Exception(f"ERROR: mode={mode} must be in ['full','light','dense'].")
        elif mode=='dense':
            # If we want to do a dense print
            self.print_dense()
        elif mode=='light':
            # If we want to do a light print
            self.print_light(
                do_print_shuffling_scores = do_print_shuffling_scores,
                do_print_last_separator   = do_print_last_separator,
            )
        elif mode=='full':
            if r!=None:
                do_print_dataset_metadata=False
                if r==0:
                    r=1 # revert to at least one rule
            if do_print_dataset_metadata:
                # dataset_metadata
                print('\ndataset_metadata :')
                print('target_name      :',self.target_name)
                print('target_goal      :',self.target_goal)
                if self.ruleset_count():
                    print('target_threshold :',self.target_threshold)
                    print('M                :',self.M)
                    print('M0               :',self.M0)
                    print('M1               :',self.M1)
            if do_print_monitoring_metadata:
                # monitoring_metadata
                print('\nmonitoring_metadata :')
                if 'p_value_min' in self.monitoring_metadata.keys():
                    print('p_value_min        :',self.monitoring_metadata['p_value_min'])
                if 'Z_score_max' in self.monitoring_metadata.keys():
                    print('Z_score_max        :',self.monitoring_metadata['Z_score_max'])
                if 'F_score_max' in self.monitoring_metadata.keys():
                    print('F_score_max        :',self.monitoring_metadata['F_score_max'])
                if 'precision_p_values' in self.monitoring_metadata.keys():
                    print('precision_p_values :',self.monitoring_metadata['precision_p_values'])
            if do_print_benchmark_scores:
                # benchmark_scores
                print('\nbenchmark_scores :')
                if ('original' in self.benchmark_scores.keys())&('shuffled' in self.benchmark_scores.keys()):
                    df_benchmark_scores_original = pd.DataFrame(data=self.benchmark_scores['original'])
                    df_benchmark_scores_shuffled = pd.DataFrame(data=self.benchmark_scores['shuffled'])
                    n_benchmark_original = len(df_benchmark_scores_original)
                    n_benchmark_shuffled = len(df_benchmark_scores_shuffled)
                    print(f'• Original ({n_benchmark_original} tests) :')
                    print(df_benchmark_scores_original)
                    print(f'• Shuffled ({n_benchmark_shuffled} tests) :')
                    print(df_benchmark_scores_shuffled)
            if do_print_rule_mining_results:
                # rule_mining_results
                if r==None:
                    print('\nrule_mining_results :')
                    print('Number of rules :',self.ruleset_count())
                if separation_width_between_rules:
                    if do_print_dataset_metadata:
                        print('\n'+separation_width_between_rules*'-')
                elif r>1:
                    print(f'Top {r} rules :')
                if self.ruleset_count():
                    range_i = self.get_range_i()
                    if r!=None:
                        if r>0:
                            range_i = range_i[:r]
                    for i in range_i:
                        if (r==None):
                            print(f'\n• Rule {i} :')
                            indentation = '\t'
                        elif r==1:
                            indentation = ''
                        else:
                            print(f'\n• Rule {i} :')
                            indentation = '\t'
                        self.i_to_print(
                            i                                = i,
                            indentation                      = indentation,
                            do_print_shuffling_scores        = do_print_shuffling_scores,
                            do_print_rule_DataFrame          = do_print_rule_DataFrame,
                            do_print_subrules_S              = do_print_subrules_S,
                            do_show_cohen_d                  = do_show_cohen_d,
                            do_show_wy_ratio                 = do_show_wy_ratio,
                            do_show_coverage_diff            = do_show_coverage_diff,
                            do_print_feature_contributions_S = do_print_feature_contributions_S,
                        )
                        if separation_width_between_rules>0:
                            print('\n'+separation_width_between_rules*'-')
                else:
                    print('No rule to show.')
    def print_light(
        self,
        print_format: str               = 'list', # 'list' or 'compact'
        do_print_shuffling_scores: bool = True,   # If we want to show the shuffling scores
        do_print_last_separator: bool   = True,   # If we want to print the last horizontal separator
    )->None:
        """
        This method does a 'light' print of the solver.
    
        Two formats:

        - ``'list'``: shows the rules via a loop of prints.
        - ``'compact'``: shows the rules in a single DataFrame.
        """
        with pd.option_context('display.max_columns', None, 'display.max_colwidth', 50, 'display.width', 1000):
            # Take the list of rules keys in the InsightSolver
            range_i = self.get_range_i()
            # Look at how many rules there are
            if len(range_i)==0:
                print("There are no rules in the InsightSolver.")
            else:
                print("----- Rule performances -----\n")
                # Handle the rules performance.
                d_i_scores = {
                    'i' : range_i,
                }
                keys = [
                    'p_value',
                    'F_score',
                    'Z_score',
                    'coverage',
                    'm1/M1',
                    'mu_rule',
                    'lift',
                    'gain',
                    'complexity_S',
                ]
                for key in keys:
                    d_i_scores[key] = [self.rule_mining_results[i][key] for i in range_i]
                # If we want to add some shuffling scores
                if do_print_shuffling_scores:
                    d_i_scores['cohen_d'] = [self.rule_mining_results[i]['shuffling_scores']['p_value']['cohen_d'] for i in range_i]
                    d_i_scores['message'] = [self.rule_mining_results[i]['shuffling_scores']['p_value']['cohen_d_message'] for i in range_i]
                # Convert the dict to a DataFrame
                df_i_scores = pd.DataFrame(d_i_scores)
                # Limit the number of digits shown for the p-value
                df_i_scores['p_value'] = df_i_scores['p_value'].apply(lambda x:format_value(value=x,format_type='scientific',decimals=6))
                # Format the gain as percentages
                df_i_scores['gain'] = df_i_scores['gain'].map(gain_to_percent)
                # Rename the complexity
                df_i_scores.rename(columns={'complexity_S':'complexity'},inplace=True)
                # Set 'i' as an index
                df_i_scores.set_index('i',inplace=True)
                # Show the result
                print(df_i_scores)

                print("\n-------- Rule details --------\n")
                # Handle the rules details
                if print_format=='compact':
                    l_df = []
                for i_rule in range_i:
                    if print_format=='list':
                        if i_rule==0:
                            print(f'i={i_rule}:')
                        else:
                            print(f'\ni={i_rule}:')

                    rule_i = self.i_to_rule(i=i_rule)
                    # Take the DataFrame of feature contributions
                    df_feature_contributions_S = self.i_to_feature_contributions_S(i=i_rule,do_ignore_col_rule_S=False)
                    df_feature_contributions_S['description'] = df_feature_contributions_S.index.map(self.columns_descr).fillna('')
                    df_feature_contributions_S = df_feature_contributions_S[['description','rule_S','p_value']]
                    df_feature_contributions_S.rename(columns={'rule_S':'rule','p_value':'contribution'},inplace=True)
                    if print_format=='compact':
                        df_feature_contributions_S.reset_index(inplace=True)
                        df_feature_contributions_S['i'] = i_rule
                        l_df.append(df_feature_contributions_S)
                    elif print_format=='list':
                        print(df_feature_contributions_S)
                if print_format=='compact':
                    df = pd.concat(
                        objs         = l_df,
                        axis         = 0,
                        ignore_index = True,
                    )
                    df = df[['i','feature_name','description','rule','contribution']]
                    print(df)
                if do_print_last_separator:
                    print("\n-----------------------------")
    def print_dense(
        self,
        do_print_lifts: bool = False,            # If we want to show the lifts
        do_print_shuffling_scores: bool = True, # If we want to show the shuffling scores
    )->None:
        """
        This method is aimed at printing a 'dense' version of the solver.
    
        Parameters
        ----------
        do_print_lifts: bool
            If we want to show the lifts.
        do_print_shuffling_scores: bool
            If we want to show the shuffling scores.
        """
        with pd.option_context('display.max_columns', 10, 'display.max_colwidth', 100, 'display.width', 1000):
            # Take the list of rules keys in the InsightSolver object.
            range_i = self.get_range_i()
            # Look at how many rules there are.
            if len(range_i)==0:
                print("There are no rules in the InsightSolver.")
            else:
                # Create a list of temporary DataFrame
                l_df_temp = []
                # Loop over the rules
                for i in range_i:
                    # Take the rule S
                    rule_S = self.i_to_S(i=i)
                    s_temp = pd.Series(rule_S,name='rule')
                    s_temp.index.name = 'variable'
                    # Add an empty row to make the view cleaner
                    s_space = pd.Series(
                        data  = [""],
                        index = pd.Series([""],name='variable'),
                        name  = 'rule',
                    )
                    s_temp = pd.concat([s_space, s_temp],axis=0)
                    df_temp = s_temp.to_frame().reset_index()
                    # Add some informations
                    df_temp['i']        = i
                    df_temp['p_value']  = self.rule_mining_results[i]['p_value']
                    df_temp['coverage'] = self.rule_mining_results[i]['coverage']
                    if do_print_lifts:
                        # If we want to add the lifts
                        df_temp['lift']     = self.rule_mining_results[i]['lift']
                    df_temp['gain']     = self.rule_mining_results[i]['gain']
                    if do_print_shuffling_scores:
                        # If we want to add the shuffling scores
                        df_temp['cohen_d'] = self.rule_mining_results[i]['shuffling_scores']['p_value']['cohen_d']
                    df_temp['']         = ''
                    l_df_temp.append(df_temp)
                # Concatenate the DataFrames
                df_concat = pd.concat(l_df_temp,axis=0,ignore_index=True)
                # Add a column "contribution"
                for i in range_i:
                    rule_S = self.i_to_S(i=i)
                    for variable in rule_S.keys():
                        contribution = self.rule_mining_results[i]['feature_contributions_S']['p_value_contribution'][variable]
                        mask  = df_concat['i'] == i
                        mask &= df_concat['variable'] == variable
                        df_concat.loc[mask, 'contribution'] = contribution
                df_concat = df_concat.sort_values(by=['i', 'contribution'], ascending=[True, False],na_position='first')
                # Manage the column 'contribution'
                #df_concat['contribution'] = df_concat['contribution'].apply(lambda x: '' if pd.isna(x) else f"{x:.2f}")
                #df_concat['contribution'] = df_concat['contribution'].apply(lambda x: '' if pd.isna(x) else f"{x * 100:.1f}%")
                df_concat['contribution'] = df_concat['contribution'].apply(lambda x: format_value(value=x,format_type='percentage',decimals=1))
                # Handle the rule's behaviour for NaNS
                df_concat['nans'] = ''
                for i in range_i:
                    rule_S = self.i_to_S(i=i)
                    for variable in rule_S.keys():
                        rule = rule_S[variable]
                        if isinstance(rule,list):
                            if len(rule)==2:
                                if rule[1] in ['exclude_nan','include_nan']:
                                    mask  = df_concat['i'] == i
                                    mask &= df_concat['variable'] == variable
                                    rule,nan = rule
                                    df_concat.loc[mask, 'nans'] = nan.split('_')[0]
                                    df_concat.loc[mask, 'rule'] = pd.Series([rule], index=df_concat.index[mask])
                # Handle the column 'lift'
                if do_print_lifts:
                    df_concat['lift'] = df_concat['lift'].round(2)
                # Handle the column 'gain'
                df_concat['gain'] = df_concat['gain'].map(gain_to_percent)
                # Handle the column 'coverage'
                #df_concat['coverage'] = df_concat['coverage'].round(3)
                #df_concat['coverage'] = df_concat['coverage'].apply(
                #   lambda x: '' if pd.isna(x) else f"{x * 100:.1f}%"
                #)
                df_concat['coverage'] = df_concat['coverage'].apply(lambda x:format_value(value=x,format_type='percentage',decimals=1))
                df_concat['coverage'] = df_concat['coverage'].apply(
                    lambda x: ' '+x if float(x[:-1])<10 else x
                )
                # Handle the column 'p_value'
                #df_concat['p_value'] = df_concat['p_value'].apply(lambda x: f"{x:.2e}")
                #df_concat['p_value'] = df_concat['p_value'].apply(lambda x: f"{x:.0e}")
                df_concat['p_value'] = df_concat['p_value'].apply(lambda x: format_value(value=x,format_type='scientific_no_decimals'))
                # Handle the column 'cohen_d'
                if do_print_shuffling_scores:
                    df_concat['cohen_d'] = df_concat['cohen_d'].round(2)
                # Put certain columns in the index
                cols_index = [
                    'i',
                    'p_value',
                    'coverage',
                ]
                if do_print_lifts:
                    cols_index.append('lift')
                cols_index.append('gain')
                if do_print_shuffling_scores:
                    cols_index.append('cohen_d')
                cols_index.append('')
                df_concat.set_index(cols_index,inplace=True)
                # Reorder some columns
                cols = ['contribution','variable','rule','nans']
                df_concat = df_concat[cols]
                # Format the DataFrame even more
                df_string = df_concat.to_string()
                lines = df_string.split('\n')
                index_columns = lines[0]        # Name of the index columns
                header = lines[1]               # Name of the main columns
                content = "\n".join(lines[2:])  # Main content
                df_string_with_spacing = f"{index_columns}\n{header}\n\n{content}"
                # Show the result
                print(df_string_with_spacing)
    def to_dict(
        self,
    )->dict:
        """
        This method aims to export the content of the solver to a dictionary.
        """
        from copy import deepcopy
        # Declare a Python dictionary
        d = dict()
        # dataset_metadata :
        d['dataset_metadata']                                       = dict()
        d['dataset_metadata']['target_threshold']                   = self.target_threshold
        d['dataset_metadata']['M']                                  = self.M
        d['dataset_metadata']['M0']                                 = self.M0
        d['dataset_metadata']['M1']                                 = self.M1
        d['dataset_metadata']['columns_names_to_descr']             = self.columns_descr
        d['dataset_metadata']['features_names_to_other_modalities'] = self.other_modalities
        # monitoring_metadata
        d['monitoring_metadata']                                    = deepcopy(self.monitoring_metadata)
        # benchmark_scores
        d['benchmark_scores']                                       = deepcopy(self.benchmark_scores)
        # rule_mining_results :
        d['rule_mining_results']                                    = deepcopy(self.rule_mining_results)
        # Return the result
        return d
    def to_json_string(
        self,
        verbose      = False,
    )->str:
        """
        This method aims to export the content of the solver to a JSON string.
        """
        # Export the solver object to a dict
        d = self.to_dict()
        # Convert the dict to a JSON string
        from .api_utilities import convert_dict_to_json_string
        json_string = convert_dict_to_json_string(d)
        # Return the result
        return json_string
    def to_dataframe(
        self,
        verbose            = False,
        do_append_datetime = False,
        do_rename_cols     = False,
    )->pd.DataFrame:
        """
        This method aims to export the content of the solver to a DataFrame.
        """
        # Handling the rules
        if verbose:
            print('Creating df_rule_mining_results...')
        df = pd.DataFrame.from_dict(
            data   = self.rule_mining_results,
            orient = 'index',
        )
        df.index.name = 'i'
        df.reset_index(inplace=True)
        cols_rule_mining_results = df.columns.to_list()
        if verbose:
            print(df)
        # Handling the metadata
        cols_metadata = [
            'target_name',                   # Dataset metadata     - str
            'target_goal',                   # Dataset metadata     - str / int
            'target_threshold',              # Dataset metadata     - int / float
            'M',                             # Dataset metadata     - int
            'M0',                            # Dataset metadata     - int
            'M1',                            # Dataset metadata     - int
            'columns_descr',                 # Dataset metadata     - dict
            'specified_constraints',         # Constraints medatada - dict
            'benchmark_scores',              # Benchmarking scores  - dict
        ]
        for col_metadata in cols_metadata:
            df[col_metadata] = len(df)*[getattr(self, col_metadata)]
        # If we want to add a datetime column to specify when the table was created
        if do_append_datetime:
            from datetime import datetime
            df['datetime_export'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Order the columns
        cols_A = [
            'datetime_export',
            'user_id',
            'target_name',
            'target_goal',
            'target_threshold',
            'M',
            'M0',
            'M1',
            'columns_descr',
            'specified_constraints',
            'benchmark_scores',
            'i',
            'm',
            'm0',
            'm1',
            'coverage',
            'm1/M1',
            'mu_rule',
            'mu_pop',
            'sigma_pop',
            'lift',
            'gain',
            'p_value',
            'F_score',
            'Z_score',
            'rule_S',
            'complexity_S',
            'F1_pop',
            'G_bad_class',
            'G_information',
            'G_gini',
            'KL_divergence',
            'p_value_ratio_S',
            'F_score_ratio_S',
            'subrules_S',
            'feature_contributions_S',
            'shuffling_scores',
            'llm',
        ]
        cols_B = df.columns.to_list()
        cols_B_minus_A = [col for col in cols_B if col not in cols_A]
        if len(cols_B_minus_A)>0:
            raise Exception(f"ERROR: Some columns are missing in the implementation : {cols_B_minus_A}")
        cols_A_inter_B = [col for col in cols_A if col in cols_B]
        df = df[cols_A_inter_B]
        # Rename some columns
        if do_rename_cols:
            """
            This renaming is useful for BigQuery:

            - Forbidden to have '/' in a column name
            - Columns names are not case sensitive, so it cannot distinguish between M and m, M0 and m0, M1 and m1.
            """
            d_rename = {
                'm1/M1' : 'coverage1', # To avoid the character '/'
                'M'     : 'm_pop',     # To avoir the collision between M and m
                'M0'    : 'm0_pop',    # To avoir the collision between M0 and m0
                'M1'    : 'm1_pop',    # To avoir the collision between M1 and m1
                'm'     : 'm_rule',    # To avoir the collision between M  and m
                'm0'    : 'm0_rule',   # To avoir the collision between M0 and m0
                'm1'    : 'm1_rule',   # To avoir the collision between M1 and m1
            }
            df.rename(
                columns = d_rename,
                inplace = True,
            )
        # Return the result
        return df
    def to_csv(
        self,
        output_file    = None,
        verbose        = False,
        do_rename_cols = False,
    )->str:
        """
        This method is meant to export the content of the solver to a CSV file.
        """
        # Avoid to generate a string containing np.float64 and np.int64 everywhere
        if np.__version__>='2.0.0':
            np.set_printoptions(legacy='1.25')
        # Export to a DataFrame
        df = self.to_dataframe(
            do_rename_cols = do_rename_cols,
        )
        if (output_file!=None)&verbose:
            print('Exporting :',output_file)
        # Create the CSV string
        csv_string = df.to_csv(output_file,index=False)
        if (output_file!=None)&verbose:
            print('Done.')
        # Return the result
        return csv_string
    def to_excel(
        self,
        output_file,
        verbose        = False,
        do_rename_cols = False,
    )->None:
        """
        This method is meant to export the solver to a Excel file.
        """
        df = self.to_dataframe(
            do_rename_cols = do_rename_cols,
        )
        if verbose:
            print('Exporting :',output_file)
        df.to_excel(
            excel_writer = output_file,
            index        = False,
            engine       = 'openpyxl',
        )
        if verbose:
            print('Done.')
    def to_excel_string(
        self,
        verbose        = False,
        do_rename_cols = False,
    )->str:
        """
        This method is meant to export the solver to a Excel string.
        """
        df = self.to_dataframe(
            do_rename_cols = do_rename_cols,
        )
        if verbose:
            print('Exporting to a Excel string...')
        # Create a buffer in memory
        import io
        excel_buffer = io.BytesIO()
        # Write df to a Excel file in the buffer
        df.to_excel(
            excel_writer = excel_buffer,
            index        = False,
            engine       = 'openpyxl',
        )
        if verbose:
            print('Done.')
        # Take the content of the buffer as bytes
        excel_bytes = excel_buffer.getvalue()
        # Convert the bytes as string
        import base64
        excel_string = base64.b64encode(excel_bytes).decode()
        # Return the result
        return excel_string
    def get_credits_needed_for_computation(
        self,
    )->int:
        """
        This method is meant to compute the number of credits for the computation during the fitting of the solver.
        """
        # Compute the number of credits needed for computation
        from .api_utilities import compute_credits_from_df
        credits_needed = compute_credits_from_df(
            df                      = self.df,
            columns_names_to_btypes = self.columns_types,
        )
        # Return the result
        return credits_needed
    def get_df_credits_infos(
        self,
        computing_source:str      = 'auto', # Where to compute the rule mining
        service_key:Optional[str] = None,   # Path+name of the service key
        user_email:Optional[str]  = None,   # User email
    )->pd.DataFrame:
        """
        This method is meant to retrieve from the server the transactions involving credits.
        """
        # Manage where the computation is executed
        if computing_source=='auto':
            computing_source='remote_cloud_function'
        # Create the outgoing dict
        d_out_credits_infos = {
            'do_compute_credits_available' : False,
            'do_compute_df_credits_infos'  : True,
        }
        # Send the dict to the API server and receive a new dict
        from .api_utilities import request_cloud_credits_infos
        d_in_credits_infos = request_cloud_credits_infos(
            computing_source       = computing_source,
            d_out_credits_infos    = d_out_credits_infos,
            input_file_service_key = service_key,
            user_email             = user_email,
        )
        # Extract the DataFrame
        df_credits_infos = d_in_credits_infos['df_credits_infos']
        # Return the result
        return df_credits_infos
    def get_credits_available(
        self,
        computing_source:str      = 'auto', # Where to compute the rule mining
        service_key:Optional[str] = None,   # Path+name of the service key
        user_email:Optional[str]  = None,   # User email
    )->int:
        """
        This method is meant to retrieve from the server the amount of credits available.
        """
        # Get the credits available
        credits_available = get_credits_available(
            computing_source = computing_source,
            service_key      = service_key,
            user_email       = user_email,
        )
        # Return the credits available
        return credits_available
    def convert_target_to_binary(
        self,
    ):
        """
        This method converts the target variable to a binary {0,1}-valued Pandas Series.

        To use this method, the attribute ``solver.target_goal`` must be populated because it specifies how to convert the target variable to binary.
        As a reminder, the target goal must be one of the following:
        
        - A modality of the target variable in the case of a categorical (i.e. ``'binary'`` or ``'multiclass'``) target variable.
        - ``'min'``, ``'min_q0'``, ``'min_q1'``, ``'min_q2'``, ``'min_q3'``, ``'min_c00'``, ``'min_c01'``, ..., ``'min_c98'``, ``'min_c99'``.
        - ``'max'``, ``'max_q1'``, ``',max_q2'``, ``'max_q3'``, ``'max_q4'``, ``'max_c01'``, ``'max_c02'``, ..., ``'max_c99'``, ``'max_c100'``.

        Returns
        -------
        s_target: pd.Series
            A {0,1}-valued Pandas Series representing the target variable.
        """
        # Take the target goal
        target_goal = self.target_goal
        if target_goal==None:
            raise Exception("ERROR: the target goal must be specified when converting a target variable to binary.")
        # Take the name of the target variable
        target_name = self.target_name
        # If the target variable's type is 'ignore', raise an Exception
        if target_name in self.columns_types and self.columns_types[target_name]=='ignore':
            raise Exception(f"ERROR: the type of the target variable '{target_name}' is 'ignore'.")
        # Take the Series of the target variable
        s = self.df[target_name].copy()
        # Create an output Pandas Series
        s_out = pd.Series(
            data  = False,
            index = s.index,
            name  = s.name,
        )
        # Handle the case where we are looking for NaNs
        if pd.isna(target_goal):
            # If we are looking for NaNs
            s_out &= s.isna()
        else:
            # If we are not looking for NaNs
            # Drop de NaNs to simplify the computation
            s.dropna(inplace=True)
            # Take the list of target modalities
            target_modalities = sorted(s.unique())
            # Look at if the target goal is in the target modalities
            if target_goal in target_modalities:
                # If the target goal is in the target modalities, we assume that the target goal is the target modality and that the target type is categorical (i.e. 'binary' or 'multiclass')
                target_modality = target_goal
                # Look at a boolean Series which indicates for which points the target value equals the target modality
                s_temp = s==target_modality
            else:
                # If the target goal is not in the target modalities, we assume that the target type is 'continuous'
                # We make sure that the target_goal is legit for a continuous target variable
                import re
                if not isinstance(target_goal,str) or (target_goal[:3] not in ['min','max']):
                    raise Exception(f"ERROR: target_goal='{target_goal}' not legitimate.")
                if target_goal[:3]=='min':
                    if target_goal=='min':
                        # If 'min' it's legit
                        # By default 'min'='min_q1'='min_c25'
                        target_threshold = np.percentile(s,25)
                    elif re.match(r"^min_q[0-3]{1}$", target_goal)!=None:
                        # If it's 'min' with a quartile 0, 1, 2, 3, it's ok (but 4 is not).
                        int_temp = int(target_goal.split('_q')[1])
                        print("\nint_temp =",int_temp)
                        if int_temp==0:
                            target_threshold = np.percentile(s,0)
                        elif int_temp==1:
                            target_threshold = np.percentile(s,25)
                        elif int_temp==2:
                            target_threshold = np.percentile(s,50)
                        elif int_temp==3:
                            target_threshold = np.percentile(s,75)
                    elif re.match(r"^min_c[0-9]{2}$", target_goal)!=None:
                        # If it's 'min' with a centile 00, 01, 02, ..., 98, 99.
                        # If 00 it's equivalent to seek for points where the target is <= the minimum of the values.
                        target_threshold = np.percentile(s,int(target_goal.split('_c')[1]))
                    else:
                        raise Exception(f"ERROR: target_goal='{target_goal}' not legitimate.")
                    # Look at which point satisfies the target threshold
                    s_temp = s.apply(lambda x:x<=target_threshold)
                elif target_goal[:3]=='max':
                    if target_goal=='max':
                        # If 'max' it's legit
                        # By default 'max'='max_q3'='max_c75'.
                        target_threshold = np.percentile(s,75)
                    elif re.match(r"^max_q[1-4]{1}$", target_goal)!=None:
                        # If it's 'max' with a quartile 1, 2, 3, 4, it's ok (but 0 is not).
                        int_temp = int(target_goal.split('_q')[1])
                        if int_temp==1:
                            target_threshold = np.percentile(s,25)
                        elif int_temp==2:
                            target_threshold = np.percentile(s,50)
                        elif int_temp==3:
                            target_threshold = np.percentile(s,75)
                        elif int_temp==4:
                            target_threshold = np.percentile(s,100)
                    elif re.match(r"^max_c[0-9]{2}$", target_goal)!=None:
                        # If it's 'max' with a 00, 01, 02, ..., 98, 99.
                        # We exclude the case where we search for values >= c00 because it's all the values.
                        if target_goal=='max_c00':
                            raise Exception(f"ERROR: target_goal='{target_goal}' not legitimate.")
                        target_threshold = np.percentile(s,int(target_goal.split('_c')[1]))
                    elif re.match(r"^max_c100$",      target_goal)!=None:
                        # If it's 'max' with a centile 100.
                        # This is equivalent to seek for points where the target variable is >= the maximum of the values.
                        target_threshold = np.percentile(s,int(target_goal.split('_c')[1]))
                    else:
                        raise Exception(f"ERROR: target_goal='{target_goal}' not legitimate.")
                    # Look at which point satisfies the target threshold
                    s_temp = s.apply(lambda x:x>=target_threshold)
                else:
                    raise Exception(f"ERROR: target_goal='{target_goal}' not legitimate.")
            # Keep only the rows where it's True
            s_temp = s_temp[s_temp]
            # Update the outgoing Pandas Series
            s_out.loc[s_temp.index] = True
        # Convert from boolean to integer
        s_out = s_out.astype(int)
        # Return the Pandas Series
        return s_out
    def compute_mutual_information(
        self,
        n_samples: int = 1000, # If we want to speed up the computation
    )->pd.Series:
        """
        This method computes the mutual information between the features and the target variable.
        The result is returned as a Pandas Series.

        Parameters
        ----------
        n_samples: int
            An integer that specifies the number of data rows to use in the computation of the mutual information.

        Returns
        -------
        s_mi: pd.Series
            A Pandas Series that contains the mutual information of the features with the target variable.
        """
        # Take the DataFrame
        df = self.df
        # Take the name of the target variable
        target_name = self.target_name
        # Sample the data if needed to speed up the computation
        if n_samples:
            if n_samples<len(df):
                df = df.sample(
                    n            = n_samples,
                    random_state = 0,
                )
        # Take all the columns of df
        cols = df.columns.to_list()
        # Remove the target column
        cols.remove(target_name)
        # Split the columns in continuous and categorical according to what is known
        columns_types    = self.columns_types
        # Split the columns in four categories
        cols_continuous  = [col for col in cols if col in columns_types and columns_types[col]=='continuous']              # Columns specified as 'continuous'
        cols_categorical = [col for col in cols if col in columns_types and columns_types[col] in ['binary','multiclass']] # Columns specified as 'binary' or 'multiclass'
        cols_ignore      = [col for col in cols if col in columns_types and columns_types[col]=='ignore']                  # Columns specified as 'ignore'
        cols_unspecified = [col for col in cols if col not in cols_continuous+cols_categorical+cols_ignore]                # Columns whose type is unspecified
        # By default, any unspecified column will be considered as continuous (so that strings will be considered alphabetically)
        cols_continuous += cols_unspecified
        # Create a DataFrame of features
        df_X = df[cols_continuous+cols_categorical].copy()
        # Create a binary Pandas Series of the target variable
        s_y = self.convert_target_to_binary().loc[df_X.index]
        # Convert continuous non numeric columns to ranks
        cols_continuous_non_numeric = df_X[cols_continuous].select_dtypes(exclude='number').columns.to_list()
        for col in cols_continuous_non_numeric:
            df_X[col] = df_X[col].astype(str).rank(method='average')
        # Hangle the missing values of the continuous numerical columns
        cols_continuous_numeric = [col for col in cols_continuous if col not in cols_continuous_non_numeric]
        for col in cols_continuous_numeric:
            if df_X[col].isna().any():
                # Fill the missing values by the median
                median = df_X[col].median()
                if pd.isna(median):  # pathological case: all the column is NaN
                    df_X[col] = 0
                else:
                    df_X[col] = df_X[col].fillna(median)
        # Set the categorical columns (numerical or non-numerical) to numbers
        for col in cols_categorical:
            df_X[col] = pd.factorize(df_X[col].astype(str))[0]
        # Take the useful categorical columns
        def is_useful_categorical_column(
            s: pd.Series,
            max_unique_absolute: int = 20,
            max_unique_ratio: float  = 0.05,
        )->bool:
            nunique = s.nunique(dropna=False)
            return (nunique <= max_unique_absolute) or (nunique / n_samples <= max_unique_ratio)
        cols_categorical_useful = [col for col in cols_categorical if is_useful_categorical_column(df_X[col])]
        # Determine the discrete features
        discrete_features = df_X.columns.isin(cols_categorical_useful)
        # Compute the mutual information
        from sklearn.feature_selection import mutual_info_classif
        mi_scores = mutual_info_classif(
            X                 = df_X,              # The features
            y                 = s_y,               # The target variable
            discrete_features = discrete_features, # Specify the categorical variables
            random_state      = 0,                 # For reproductibility
            n_jobs            = -1,                # Use all CPU
            n_neighbors       = 4,
        )
        # Convert the result to a Pandas Series
        s_mi = pd.Series(
            data  = mi_scores,
            index = df_X.columns,
            name  = 'mutual_info',
        ).sort_values(ascending=False)
        # Return the mutual information
        return s_mi
    def plot(
        self,
        language: str = "en",
        do_mutual_information: bool   = True,
        do_banner: bool               = True,
        do_contributions: bool        = True,
        do_distributions: bool        = True,
        do_mosaics_rule_vs_comp: bool = True,
        do_mosaics_rule_vs_pop: bool  = True,
        do_legend: bool               = True,
    ) -> None:
        """
        Displays all visualization figures for the solver.

        Parameters
        ----------
        language : str
            Language for the plots ('en' or 'fr').
        do_mutual_information : bool
            Whether to show the mutual information figure.
        do_banner : bool
            Whether to show the banner figures.
        do_contributions : bool
            Whether to show feature contributions.
        do_distributions : bool
            Whether to show feature distributions.
        do_mosaics_rule_vs_comp : bool
            Whether to show the mosaics of rule vs complement figures.
        do_mosaics_rule_vs_pop : bool
            Whether to show the mosaics of rule vs population figures.
        do_legend : bool
            Whether to show the legend figure.
        """
        from .visualization import plot_all
        plot_all(
            solver                  = self,
            language                = language,
            do_mutual_information   = do_mutual_information,
            do_banner               = do_banner,
            do_contributions        = do_contributions,
            do_distributions        = do_distributions,
            do_mosaics_rule_vs_comp = do_mosaics_rule_vs_comp,
            do_mosaics_rule_vs_pop  = do_mosaics_rule_vs_pop,
            do_legend               = do_legend,
        )
    def to_pdf(
        self,
        output_file: Optional[str]    = None,
        verbose: bool                 = False,
        do_mutual_information: bool   = True,
        do_banner: bool               = True,
        do_contributions: bool        = True,
        do_distributions: bool        = True,
        do_mosaics_rule_vs_comp: bool = True,
        do_mosaics_rule_vs_pop: bool  = True,
        do_legend: bool               = True,
        language: str                 = "en",
    ):
        """
        Export a PDF file containing various results and figures of the solver.

        This method is now a simple wrapper around visualization.make_pdf().

        Parameters
        ----------
        output_file : str, optional
            Path where the PDF should be exported.
        verbose : bool, default False
            Verbosity.
        do_mutual_information : bool
            Include mutual information figure.
        do_banner : bool
            Include banner figures.
        do_contributions : bool
            Include contribution figures.
        do_distributions : bool
            Include distribution figures.
        do_mosaics_rule_vs_comp : bool
            Include mosaics of rule vs complement figures.
        do_mosaics_rule_vs_pop : bool
            Include mosaics of rule vs population figures.
        do_legend : bool
            Include the legend figure.
        language : str
            Language for the plots ('en' or 'fr').

        Returns
        -------
        pdf_base64 : str
            The PDF content encoded as a base64 string, suitable for in-memory use.
        """
        from .visualization import make_pdf
        pdf_base64 = make_pdf(
            solver                  = self,
            output_file             = output_file,
            verbose                 = verbose,
            do_mutual_information   = do_mutual_information,
            do_banner               = do_banner,
            do_contributions        = do_contributions,
            do_distributions        = do_distributions,
            do_mosaics_rule_vs_comp = do_mosaics_rule_vs_comp,
            do_mosaics_rule_vs_pop  = do_mosaics_rule_vs_pop,
            do_legend               = do_legend,
            language                = language,
        )
        return pdf_base64
    def to_zip(
        self,
        output_file: Optional[str] = None,
        verbose: bool = False,
        do_png: bool = True,
        do_csv: bool = True,
        do_json: bool = True,
        do_excel: bool = True,
        do_pdf: bool = True,
        language: str = "en",
    ):
        """
        Export the solver content to a ZIP file.

        This method is now a simple wrapper around visualization.make_zip().
        """
        from .visualization import make_zip
        zip_base64 = make_zip(
            solver      = self,
            output_file = output_file,
            verbose     = verbose,
            do_png      = do_png,
            do_csv      = do_csv,
            do_json     = do_json,
            do_excel    = do_excel,
            do_pdf      = do_pdf,
            language    = language,
        )
        return zip_base64

################################################################################
################################################################################
