"""Version information for `setup.py`."""

# ruff: noqa: E501
#   ____  _ _    __                   _
#  | __ )(_) |_ / _| ___  _   _ _ __ | |_
#  |  _ \| | __| |_ / _ \| | | | '_ \| __|
#  | |_) | | |_|  _| (_) | |_| | | | | |_
#  |____/|_|\__|_|  \___/ \__,_|_| |_|\__|
from __future__ import annotations

from datetime import datetime, timezone

current_year = datetime.now(timezone.utc).year

__author__ = "Bitfount"
__author_email__ = "info@bitfount.com"
__copyright__ = f"Copyright {current_year} Bitfount Ltd"
__description__ = "Machine Learning and Federated Learning Library."
__title__ = "bitfount"
__url__ = "https://github.com/bitfount/bitfount"
__version__ = "9.0.0"

# Legacy combined version list - maintained for backward compatibility
# YAML versions must be all on one line for the breaking changes script to work
__yaml_versions__ = ["2.0.0", "3.0.0", "4.0.0", "4.0.1", "4.1.0", "5.0.0", "6.0.0", "6.1.0", "6.2.0", "6.2.1", "6.3.0", "6.4.0", "6.5.0", "6.6.0"]  # fmt: off

# Role-specific version lists - starting fresh with 7.0.0
__modeller_yaml_versions__ = ["7.0.0", "7.1.0", "7.2.0", "7.3.0", "7.4.0", "7.5.0", "7.6.0", "7.7.0", "7.8.0", "7.9.0", "7.10.0", "7.11.0", "7.12.0", "7.13.0", "7.14.0", "7.15.0", "7.16.0", "7.17.0", "7.17.1", "7.18.0", "7.19.0", "7.20.0", "7.21.0", "7.22.0", "7.23.0", "7.24.0", "7.25.0", "7.26.0", "7.27.0", "7.28.0", "7.29.0", "7.30.0", "7.30.1", "7.31.0", "7.32.0", "7.33.0", "7.34.0", "7.35.0", "7.36.0", "7.37.0", "7.37.1", "7.38.0", "7.39.0", "7.40.0", "7.41.0", "7.42.0", "7.43.0", "7.44.0", "7.45.0", "7.46.0", "7.47.0", "7.48.0", "7.49.0", "7.50.0", "7.51.0", "7.52.0", "7.53.0", "7.54.0", "7.55.0"]  # fmt: off

# Use semver conventions for the YAML versions
# YAML Version Changes
__changelog__ = """
- 7.55.0:
    - Added PatientIDExchangeAlgorithm for exchanging patient IDs during initial setup phase.
    - Updated DataExtractionProtocolCharcoal to use PatientIDExchangeAlgorithm instead of requiring patient IDs as protocol arguments.
    - Updated data_extraction_charcoal.yaml task template to include PatientIDExchangeAlgorithm as the first algorithm with patient_ids and patient_ids_file template variables.
    - Added FHIR capabilities to EHRPatientInfoDownloadAlgorithm.
    - DataExtractionProtocolCharcoal now uses S3UploadAlgorithm to upload the results.
- 7.54.0:
    - Added Scan Frequency Filter Strategy to Record Filter Algorithm.
- 7.53.0:
    - Added NullSource.
- 7.52.0:
    - Added Patient ID Filter Strategy to Record Filter Algorithm.
    - Improved typing by replacing types with enums where relevant
- 7.51.0:
    - Added PrivateSqlQuery Algorithm.
- 7.50.0:
    - Made group_by a required arg from batch grouping.
- 7.49.0:
    - _WetAMDScreeningProtocolSapphire is now WetAMDScreeningProtocolSapphire.
- 7.48.0:
    - Changed batch grouping to be a template field in _WetAMDScreeningProtocolSapphire.
- 7.47.0:
    - Added Sapphire Trial Inclusion Algorithm
- 7.46.0:
    - Added Longitudinal Algorithm
- 7.45.0:
    - Expanded the Charcoal Trial Inclusion Criteria to include more criteria.
- 7.44.0:
    - Add batch grouping to _WetAMDScreeningProtocolSapphire.
- 7.43.0:
    - Added Topcon datasource
- 7.42.0:
    - Added InterMine datasource
- 7.41.0:
    - Added CSTCalculationAlgorithm for Central Subfield Thickness calculation.
- 7.40.0:
    - Added _WetAMDScreeningProtocolSapphire protocol for Wet-AMD screening
- 7.39.0:
    - Renaming of NextGenPatientInfoDownloadAlgorithm to EHRPatientInfoDownloadAlgorithm
- 7.38.0:
    - Introduction of ImageSelectionAlgorithm.
- 7.37.1:
    - Allow ReduceCSVAlgorithmCharcoal to have templated variables.
- 7.37.0:
    - Added parameters to ReduceCSVAlgorithmCharcoal: eligible_only and delete_intermediate
- 7.36.0:
    - Introduction of S3UploadAlgorithm.
- 7.35.0:
    - Added enable_anonymized_tracker_upload to task definition. If missing, it will default to False.
- 7.34.0:
    - Deprecated save_path arguments in various algorithm schemas.
- 7.33.0:
    - Addition of argument back to EHRPatientQueryAlgo
- 7.32.0:
    - Added ehr_config in pod config
    - Removal of URL arguments to EHRPatientQueryAlgo
- 7.31.0:
    - Added exclusion codes to TrialInclusionCriteriaMatchAlgorithmBronze
- 7.30.1:
    - Fixed a bug in the types of some templated fields.
- 7.30.0:
    - Added support for templated strings in the YAML configs.
- 7.29.0:
    - Added support for saving results to a file to ResultsOnly protocol
    - Added support for running SQL query remotely to SqlQuery algorithm
- 7.28.0:
    - Changed NextGenPatientQueryAlgo to generic EHRPatientQueryAlgo (not a breaking change
      as there are no references to NextGenPatientQueryAlgo are out in the wild yet)
- 7.27.0:
    - Added support for indicating whether to re-run or not a task on previously failed files.
- 7.26.0:
    - Add FluidVolumeScreeningProtocol
- 7.25.0:
    - Added OMOP datasource
- 7.24.0:
    - Adds the ability for multiple secrets to be supplied in the YAML configs, with
      their intended usage being specified in the YAML.
- 7.23.0:
    - Removes JWT-based authentication from the YAML configs. This is not a breaking
      change as this was never actually working from the YAML due to the need for the
      JWT to have a callback specified.
- 7.22.0:
    - Add FluidVolumeCalculationAlgorithm
- 7.21.0:
    - Added new protocol GAScreeningProtocolBronzeWithEHRConfig
    - Added aux_col as argument to CSVReportGeneratorOphthalmologyAlgorithmArgumentsConfig
- 7.20.0:
    - Added inclusion and exclusion codes as input to TrialInclusionCriteriaMatchAlgorithmCharcoal
- 7.19.0:
    - Add InSite Insights protocol
- 7.18.0:
    - Add user defined primary_results_path
- 7.17.1:
    - Removed ICD10/CPT4 arguments from NextGenPatientQueryAlgorithm
- 7.17.0:
    - Add GAScreeningProtocolCharcoal protocol
- 7.16.0:
    - Add more configurable options to BscanImageAndMaskGenerationAlgorithm
- 7.15.0:
    - Add DataExtractionProtocolCharcoal protocol
- 7.14.0:
    - Add NextGenPatientInfoDownloadAlgorithm
- 7.13.0:
    - Add support for iterative splitting to PercentageSplitter
- 7.12.0:
    - Add support for test_runs as part of the modeller config.
- 7.11.0:
    - Add Reduced CSV Algorithm for Charcoal
- 7.10.0:
    - Add fovea capabilities to Charcoal algorithm
- 7.9.0:
    - Add Config for Charcoal Trial Inclusion
- 7.8.0:
    - Adds support for boolean as task template variables.
- 7.7.0:
  - Added InferenceAndImageOutput protocol
- 7.6.0:
  - Introduced new bscan image and mask generation algorithm.
- 7.5.0:
  - Add largest lesion upper size bound and patient age bounds to trial inclusion algorithms.
- 7.4.0:
   - Added post-processing to ModelInference Algorithm.
- 7.3.0:
  - Amethyst to use Amethyst Trial Calculation
  - Addition of Charcoal Trial Calculation
- 7.2.0:
  - Adding Image Source
- 7.1.0:
    Modeller:
        - Introduced new pre-filtering algorithm.
- 7.0.0:
  - Complete redesign of YAML versioning system
  - Introduced role-specific version lists (__pod_yaml_versions__ and __modeller_yaml_versions__)
  - Decoupled pod and modeller configuration schemas
  - Maintained backward compatibility with __yaml_versions__ for legacy code
  - Reset version numbering for role-specific schemas to provide a clean starting point
- 6.6.0:
  - Add specifications for datasource and datasplitter (kw)arg dictionaries,
    to provide tighter specification of these items.
  - Fix typing of "save path", etc., instances to correctly be specced as string/null
    rather than types inferred from fields.Function()
  - Fix Optional[Union[X, Y]] specs to correctly allow None/null
  - Change Union parsing to export to anyOf instead of oneOf, to better match
    the expected Marshmallow behaviour.
  - Fix issue with Union[dict[...],...] fields not being correctly written to
    the spec if they didn't contain enums.
  - Fix enum dicts to ensure they are valid JSON Schema components.
  - Introduce typing for template elements to ensure that those are also adhered to.
- 6.5.0:
  - Added NextGenSearchProtocol protocol
  - Fix incorrect args config for _SimpleCSVAlgorithm
- 6.4.0:
  - Added NextGenPatientQuery algorithm
"""
