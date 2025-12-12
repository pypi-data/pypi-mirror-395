from typing import Annotated, Literal

from pydantic import AfterValidator
from sqlalchemy.types import TypeDecorator, Unicode

from cidc_api.reference.icdo3 import is_ICDO3_code, is_ICDO3_term
from cidc_api.reference.uberon import is_uberon_term
from cidc_api.reference.ctcae import (
    is_ctcae_event_term,
    is_ctcae_event_code,
    is_ctcae_severity_grade,
    is_ctcae_system_organ_class,
)
from cidc_api.reference.icd10cm import (
    is_ICD10CM_code,
    is_ICD10CM_term,
)
from cidc_api.reference.gvhd import is_gvhd_organ

# As python Enums are rather cumbersome when we only want a list of permissible values for a string, use Literal instead


TrialOrganization = Literal[
    "ECOG-ACRIN",
    "SWOG",
    "NRG",
    "ETCTN",
]


TrialFundingAgency = Literal[
    "Broad Institute",
    "Center for Biomedical Informatics and Information Technology",
    "Center for Inherited Disease Research",
    "Department of Defense",
    "Division of Cancer Control and Population Sciences",
    "Evelyn H. Lauder Founder’s Fund for Metastatic Breast Cancer Research",
    "Food and Drug Administration",
    "Foundation Medicine Inc",
    "Georgetown Lombardi Comprehensive Cancer Center",
    "Knight Cancer Institute",
    "Leukemia and Lymphoma Society",
    "Multiple Myeloma Research Foundation",
    "National Cancer Institute",
    "National Clinical Trials Network",
    "National Institutes of Health",
    "National Library of Medicine",
    "NCI Center for Cancer Research",
    "Proteogenomic Translational Research Centers",
    "Purdue University Center for Cancer Research",
    "Transplant Recipients International Organization",
    "UNC Lineberger Comprehensive Cancer Center",
]


AssayType = Literal[
    "Olink",
    "WES",
    "BD Rhapsody",
    "GeoMx",
    "RNAseq",
    "IHC",
    "CyTOF",
    "H&E",
    "ELISA",
    "EVP",
    "mIF",
    "mIHC",
    "MALDI Glycan",
    "TCRseq",
    "ATACseq",
    "ctDNA",
    "Microbiome",
    "Nanostring",
    "NULISA",
    "MIBI",
    "scRNAseq",
    "snRNA-Seq",
    "Visium",
    "Olink HT",
]


AdministrativeRole = Literal[
    "Principal Investigator",
    "Contact",
    "Staff",
]


Sex = Literal[
    "Male",
    "Female",
    "Unknown",
]


AgeAtEnrollmentUnits = Literal["Days", "Years"]


Race = Literal[
    "American Indian or Alaska Native",
    "Asian",
    "Black or African American",
    "Native Hawaiian or other Pacific Islander",
    "Not allowed to collect",
    "Not Reported",
    "Unknown",
    "White",
]


Ethnicity = Literal[
    "Hispanic or Latino",
    "Not allowed to collect",
    "Not Hispanic or Latino",
    "Not reported",
    "Unknown",
]


HeightUnits = Literal[
    "ft",
    "in",
    "m",
    "cm",
]


WeightUnits = Literal[
    "lb",
    "g",
    "kg",
]


BodySurfaceAreaUnits = Literal[
    "ft2",
    "in2",
    "m2",
    "cm2",
]


Occupation = Literal[
    "Armed Forces Occupations",
    "Clerical support workers",
    "Craft and Related Trades Worker",
    "Elementary Occupation",
    "Manager",
    "Other",
    "Plant and Machine Operators and Assemblers",
    "Professional",
    "Service and Sales Workers",
    "Skilled Agricultural, Forestry, and Fishery Workers",
    "Technicians and Associate Professionals",
]


Education = Literal[
    "Bachelor's Degree",
    "Choose not to disclose",
    "Data not available",
    "Doctoral degree or professional degree",
    "Grade School",
    "Graduate or professional degree",
    "High school graduate (including equivalency)",
    "Master's Degree",
    "No formal education",
    "Not Applicable",
    "Not high school graduate",
    "Some college or associate degree",
    "Some training after high school",
]


OffStudyReason = Literal[
    "Completion of Follow-Up",
    "Completion of Planned Therapy",
    "Death",
    "Disease Progression",
    "Failure to Attain Remission",
    "Ineligible",
    "Lost to Follow-Up",
    "Not Reported",
    "Other",
    "Physician Decision",
    "Relapse",
    "Secondary Malignancy",
    "Study Discontinuation",
    "Subject Non-Compliance",
    "Subject/Guardian Refused Further Treatment",
    "Toxicity",
    "Unknown",
    "Withdrawal of Consent",
]


ChecksumType = Literal["md5",]


FileFormat = Literal[
    "CSV",
    "DOC",
    "DOCX",
    "TSV",
    "TXT",
    "XLS",
    "XLSX",
]


TumorGrade = Literal[
    "G1 Low Grade",
    "G2 Intermediate Grade",
    "G3 High Grade",
    "G4 Anaplastic",
    "GB Borderline",
    "GX Grade Cannot Be Assessed",
    "Not Applicable",
    "Not Reported",
    "Unknown",
]

CancerStageSystem = Literal[
    "AJCC",
    "R-ISS",
    "FIGO",
    "Not Applicable",
]


CancerStageSystemVersionAJCC = Literal["8th Edition",]

CancerStageSystemVersionRISS = Literal["10.1200/JCO.2015.61.2267"]

CancerStageSystemVersionFIGO = Literal[
    "10.1002/ijgo.14923",
    "10.1002/ijgo.13881",
    "10.1002/ijgo.13867",
    "10.1002/ijgo.13865",
    "10.1002/ijgo.13866",
    "10.1002/ijgo.13878",
    "10.1002/ijgo.13877",
    "10.1002/ijgo.12613",
]

CancerStageSystemVersion = CancerStageSystemVersionAJCC | CancerStageSystemVersionFIGO | CancerStageSystemVersionRISS

CancerStageAJCC = Literal[
    "Stage 0",
    "Stage 0a",
    "Stage 0is",
    "Stage I",
    "Stage IA",
    "Stage IA1",
    "Stage IA2",
    "Stage IA3",
    "Stage IB",
    "Stage IB1",
    "Stage IB2",
    "Stage II",
    "Stage IIA",
    "Stage IIA1",
    "Stage IIA2",
    "Stage IIB",
    "Stage IIC",
    "Stage III",
    "Stage IIIA",
    "Stage IIIB",
    "Stage IIIC",
    "Stage IS",
    "Stage IV",
    "Stage IVA",
    "Stage IVB",
    "Stage IVC",
    "Stage occult carcinoma",
]


CancerStageFIGO = Literal[
    "value",
    "Stage I",
    "Stage IA",
    "Stage IA1",
    "Stage IA2",
    "Stage IA3",
    "Stage IB",
    "Stage IC",
    "Stage II",
    "Stage IIA",
    "Stage IIB",
    "Stage IIC",
    "Stage III",
    "Stage IIIA",
    "Stage IIIA1",
    "Stage IIIA2",
    "Stage IIIB",
    "Stage IIIB1",
    "Stage IIIB2",
    "Stage IIIC",
    "Stage IIIC1",
    "Stage IIIC1i",
    "Stage IIIC1ii",
    "Stage IIIC2",
    "Stage IIIC2i",
    "Stage IIIC2ii",
    "Stage IV",
    "Stage IVA",
    "Stage IVB",
    "Stage IVC",
    "Stage IB1",
    "Stage IB2",
    "Stage IB3",
    "Stage IIA1",
    "Stage IIA2",
    "Stage IC1",
    "Stage IC2",
    "Stage IC3",
    "Stage IIIA1(i)",
    "Stage IIIA1(ii)",
]


CancerStageRISS = Literal["Stage I"]  # TODO

CancerStage = CancerStageAJCC | CancerStageFIGO | CancerStageRISS


TCategory = Literal[
    "cT0",
    "cT4",
    "cTis",
    "cTX",
    "pT2a",
    "pT2b",
    "pT3a",
    "pT3b",
    "T0",
    "T1",
    "T1a",
    "T1a1",
    "T1a2",
    "T1b",
    "T1b1",
    "T1b2",
    "T1c",
    "T1d",
    "T1mi",
    "T2",
    "T2a",
    "T2a1",
    "T2a2",
    "T2b",
    "T2c",
    "T2d",
    "T3",
    "T3a",
    "T3b",
    "T3c",
    "T3d",
    "T4",
    "T4a",
    "T4b",
    "T4c",
    "T4d",
    "T4e",
    "Ta",
    "Tis",
    "Tis (DCIS)",
    "Tis (Paget)",
    "TX",
    "Not Reported",
    "Unknown",
]


NCategory = Literal[
    "cN0",
    "cN1",
    "cN1mi",
    "cN2",
    "cN2a",
    "cN2b",
    "cN3",
    "cN3a",
    "cN3b",
    "cN3c",
    "cNX",
    "N0",
    "N0(i+)",
    "N0a",
    "N0b",
    "N1",
    "N1a",
    "N1b",
    "N1c",
    "N2",
    "N2a",
    "N2b",
    "N2c",
    "N3",
    "N3a",
    "N3b",
    "N3c",
    "NX",
    "Not Reported",
    "Unknown",
]


MCategory = Literal[
    "cM0",
    "cM0(i+)",
    "cM1",
    "cM1a",
    "cM1a(0)",
    "cM1a(1)",
    "cM1b",
    "cM1b(0)",
    "cM1b(1)",
    "cM1c",
    "cM1c(0)",
    "cM1c(1)",
    "cM1d",
    "cM1d(0)",
    "cM1d(1)",
    "M0",
    "M1",
    "pM1",
    "Not Reported",
    "Unknown",
]


YNU = Literal[
    "Yes",
    "No",
    "Unknown",
]


YNUNA = Literal[
    "Yes",
    "No",
    "Unknown",
    "Not Applicable",
]


UberonAnatomicalTerm = Annotated[str, AfterValidator(is_uberon_term)]
ICDO3MorphologicalCode = Annotated[str, AfterValidator(is_ICDO3_code)]
ICDO3MorphologicalTerm = Annotated[str, AfterValidator(is_ICDO3_term)]


SurvivalStatus = Literal[
    "Alive",
    "Dead",
    "Unknown",
]


CauseOfDeath = Literal[
    "Accidental death",
    "Acute GVHD",
    "Adult Respiratory Distress Syndrome (ARDS)",
    "Adverse Event",
    "APL Differentiation Syndrome",
    "Aspiration Pneumonia",
    "Bacterial infection",
    "BCNU IP",
    "Cancer Related",
    "Cardiac Disease",
    "Cardiac failure",
    "Cardiopulmonary Arrest",
    "Cardiovascular accident",
    "Cardiovascular Disorder",
    "Central nervous system(CNS) failure",
    "Chronic GVHD",
    "Chronic liver disease",
    "Chronic Obstructive Pulmonary Disease",
    "Congestive Heart Failure",
    "Coronary artery disease (atherosclerosis)",
    "Dementia  (including Alzheimer's disease)",
    "Diabetes Mellitus",
    "Disseminated intravascular coagulation (DIC)",
    "Drug Related",
    "End-stage Renal Disease",
    "Failure to Thrive",
    "Fungal infection",
    "Gastrointestinal (GI) failure (not liver)",
    "Gastrointestinal hemorrhage",
    "Graft rejection or failure",
    "Graft Versus Host Disease",
    "Hemorrhage",
    "Hemorrhage, not otherwise specified",
    "Hemorrhagic cystitis",
    "Hepatitis",
    "Herpes",
    "HIV/AIDS",
    "Immunotherapy-Related",
    "Infection",
    "Infection, NOS",
    "Infection, organism not identified",
    "Influenza",
    "Interstitial Pneumonia (IP) NOS",
    "Intracranial hemorrhage",
    "IPS, idiopathic",
    "IPS, viral, cytomegalovirus(CMV)",
    "IPS, viral, other",
    "Liver failure (not VOD)",
    "Multiple Organ Failure",
    "Myocardial infarction",
    "Natural causes",
    "Non-protocol cancer therapy",
    "Not Cancer Related",
    "Not Reported",
    "Organ failure, not otherwise specified",
    "Other cause",
    "Parkinson's Disease",
    "Persistence or recurrence of underlying disease",
    "Pneumonia NOS",
    "Prior malignancy",
    "Protozoal infection",
    "Pulmonary Disease",
    "Pulmonary Embolism",
    "Pulmonary failure",
    "Pulmonary hemorrhage",
    "Radiation IP",
    "Recurrence/persistence/progression of disease reported for first HSCT",
    "Renal Disorder, NOS",
    "Renal failure",
    "Respiratory failure",
    "Sepsis",
    "Sinusoidal Obstruction Syndrome",
    "Spinal Muscular Atrophy",
    "Suicide",
    "Surgical Complication",
    "Thromboembolic",
    "Thrombosis",
    "Thrombotic thrombocytopenic purpura (HUS/TTP)",
    "Toxicity",
    "Unacceptable Toxicity",
    "Unclassified infection / Infection NOS",
    "Unknown",
    "Vascular, not otherwise specified",
    "Veno-occlusive disease (VOD) / sinusodial obstruction syndrome (SOS)",
    "Viral infection",
    "VOD",
]


ResponseSystem = Literal[
    "RECIST",
    "iRECIST",
]


ResponseSystemVersionRecist = Literal["1.1"]
ResponseSystemVersionIrecist = Literal["10.1016/S1470-2045(17)30074-8"]  # DOI version
ResponseSystemVersion = ResponseSystemVersionRecist | ResponseSystemVersionIrecist

BestOverallResponseRecist = Literal[
    "Complete Response", "Partial Response", "Progressive Disease", "Stable Disease", "Not available", "Not assessed"
]
BestOverallResponseIrecist = Literal[
    "immune Complete Response",
    "immune Partial Response",
    "immune Stable Disease",
    "immune Unconfirmed Progressive Disease",
    "immune Confirmed Progressive Disease",
    "Not available",
    "Not assessed",
]
BestOverallResponse = BestOverallResponseRecist | BestOverallResponseIrecist


SpecimenType = Literal[
    "BAL Cells",
    "BAL Cell Supernatant",
    "BAL Fluid",
    "BMMC",
    "BMMC Supernatant",
    "Bone Marrow Aspirate",
    "Bone Marrow Core",
    "Bone Marrow Film",
    "Buccal Cells",
    "Buffy Coat",
    "CAR-T Cells",
    "cfDNA",
    "CSF",
    "CSF Cells",
    "CSF Cell Supernatant",
    "CTC Cells",
    "CTC Cell Supernatant",
    "ctDNA",
    "Cytospin Film",
    "DNA",
    "FFPE Block",
    "FFPE Block Punch",
    "FFPE Section",
    "FFPE Tissue Core",
    "FFPE Tissue Curl",
    "FFPE Tissue Scroll",
    "Fine Needle Aspirate",
    "Fixed Tissue Slide",
    "Formalin Fixed Tissue",
    "Fresh Tissue",
    "Fresh Tissue Core",
    "Frozen Tissue",
    "Frozen Tissue Block",
    "Frozen Tissue Curl",
    "Frozen Tissue Core",
    "Frozen Tissue Section",
    "Germline DNA",
    "Germline Nucleic Acid",
    "Germline RNA",
    "H&E Fixed Tissue Slide",
    "Leukapheresis Cells",
    "Lymph Node Tissue",
    "Nucleic Acid",
    "OCT Frozen Tissue",
    "OCT Frozen Tissue Block",
    "OCT Frozen Tissue Core",
    "OCT Frozen Tissue Curl",
    "OCT Frozen Tissue Section",
    "PBMC",
    "PBMC Supernatant",
    "PBSC",
    "PBSC Supernatant",
    "Peptides",
    "Pericardial Fluid",
    "Peritoneal Cells",
    "Peritoneal Cell Supernatant",
    "Peritoneal Fluid",
    "Peritoneal Lavage Fluid",
    "Plasma",
    "Pleural Cells",
    "Pleural Cell Supernatant",
    "Pleural Fluid",
    "Protein Lysate",
    "RNA",
    "Saliva",
    "Serum",
    "Skin Tissue",
    "Stool",
    "Synovial Fluid",
    "Tissue Core",
    "Urine",
    "WBC",
    "Whole Blood",
    "Whole Blood Film",
    "Other",
]


SpecimenDescription = Literal["Tumor", "Normal"]


TumorType = Literal["Metastatic Tumor", "Primary Tumor", "Not Reported"]


CollectionProcedure = Literal[
    "Fine Needle Aspiration",
    "Phlebotomy",
    "Bone Marrow Aspiration",
    "Bone Marrow Core Biopsy",
    "Core Biopsy",
    "Endoscopic Biopsy",
    "Surgical Excision",
    "Fine Needle Aspiration",
    "Lumbar Puncture",
    "FFPE Block Punch Biopsy",
    "Skin Biopsy",
    "Apheresis",
    "Bone Biopsy",
    "Bronchoalveolar Lavage",
    "Buccal Swab",
    "Leukapheresis",
    "Mid Stream Urine Collection",
    "Peritoneal Lavage",
    "Peritoneal Paracentesis",
    "Pleural Thoracentesis",
    "Saliva Collection",
    "Stool Collection",
    "Surgical Incision",
    "Urine Voiding",
    "Not Reported",
    "Other",
]


FixationStabilizationType = Literal[
    "Ficoll",
    "Formalin Fixation",
    "Formalin-Fixed Paraffin-Embedded (FFPE)",
    "Frozen",
    "70% Ethanol",
    "H&E",
    "Liquid Nitrogen (Frozen)",
    "OCT (Frozen)",
    "Proteomic Stabilization",
    "Thaw-Lyse",
    "Not Reported",
    "Other",
]


PrimaryContainerType = Literal[
    "ACD-A Tube",
    "ACD-B Tube",
    "Bag",
    "Box",
    "CellSave Tube",
    "Conical Tube",
    "Container",
    "CPT Citrate Tube",
    "CPT Heparin Tube",
    "Cryovial",
    "EDTA Tube",
    "Fecal Collection Container with NA Stabilizer",
    "FFPE Tissue Cassette",
    "Formalin Jar",
    "Lithium Heparin Tube",
    "OMNIgene",
    "OMNImet",
    "PAXgene DNA Tube",
    "PAXgene RNA Tube",
    "Plain Red Top Tube",
    "PPT Tube",
    "Saliva Tube",
    "Screw Top Jar",
    "Slide",
    "Slide Cassette",
    "Smart Tube",
    "Sodium Citrate Tube",
    "Sodium Heparin Tube",
    "SST Tube",
    "Streck Tube",
    "Other",
]


VolumeUnits = Literal[
    "Microliters",
    "Milliliters",
    "Not Reported",
    "Other",
]


ProcessedType = Literal[
    "BAL Cells",
    "BAL Cell Supernatant",
    "BMMC",
    "BMMC Supernatant",
    "Bone Marrow Film",
    "Buccal Cells",
    "Buffy Coat",
    "cfDNA",
    "CSF Cell Supernatant",
    "CSF Cells",
    "CTC Cell Supernatant",
    "CTC Cells",
    "ctDNA",
    "DNA",
    "FFPE Block",
    "FFPE Block Punch",
    "FFPE Section",
    "FFPE Tissue Core",
    "FFPE Tissue Curl",
    "FFPE Tissue Scroll",
    "Formalin Fixed Tissue",
    "Germline DNA",
    "Germline RNA",
    "Leukapheresis Cells",
    "Other",
    "PBMC",
    "PBMC Supernatant",
    "PBSC",
    "PBSC Supernatant",
    "Peritoneal Cell Supernatant",
    "Peritoneal Cells",
    "Plasma",
    "Pleural Cell Supernatant",
    "Pleural Cells",
    "RNA",
    "Serum",
    "Whole Blood Film",
    "Protein Lysate",
    "Peptides",
    "Germline Nucleic Acid",
    "Nucleic Acid",
    "H&E Fixed Tissue Slide",
    "Fixed Tissue Slide",
    "WBC",
]


ConcentrationUnits = Literal[
    "Nanogram per Microliter",
    "Milligram per Milliliter",
    "Micrograms per Microliter",
    "Cells per Vial",
    "Not Reported",
    "Other",
]


DerivativeType = Literal[
    "cfDNA",
    "ctDNA",
    "Germline DNA",
    "Germline RNA",
    "Other",
    "Protein Lysate",
    "Peptides",
    "Tumor DNA",
    "Tumor RNA",
    "Stool DNA",
]

PBMCRestingPeriodUsed = Literal[
    "Yes",
    "No",
    "Not Reported",
    "Other",
]


MaterialUnits = Literal[
    "Microliters",
    "Milligrams",
    "Milliliters",
    "Nanogram per Microliter",
    "Milligram per Milliliter",
    "Micrograms per Microliter",
    "Cells per Vial",
    "Slides",
    "Not Reported",
    "Other",
]


MaterialStorageCondition = Literal[
    "Ambient",
    "RT",
    "4 Celsius Degree",
    "-20 Degrees Celsius Or Minus 20 Degrees Celsius",
    "-80 Degrees Celsius Or Minus 80 Degrees Celsius",
    "-150 Degrees Celsius Or Minus 150 Degrees Celsius",
    "LN",
    "Dry Ice",
    "Not Reported",
    "Other",
]


QCCondition = Literal[
    "QC Pass",
    "Pass at Risk",
    "QC Failed",
    "QC Lost",
    "QC Not Shipped",
]


ReplacementRequested = Literal[
    "Replacement Not Requested", "Replacement Requested", "Replacement Tested", "Not Reported", "Other"
]


ResidualUse = Literal[
    "Sample Returned", "Sample Sent to Another Lab", "Sample received from CIMAC", "Not Reported", "Other"
]


DiagnosisVerification = Literal[
    "Local pathology review was not consistent",
    "Local pathology review was consistent with site of tissue procurement diagnostic pathology report",
    "Not Available",
    "Not Reported",
    "Other",
]


AssayPriority = Literal[
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "Not Reported",
    "Other",
]


Courier = Literal["FedEx", "USPS", "UPS", "Inter-Site Delivery", "DHL"]


ShipmentCondition = Literal["Frozen Dry Ice", "Frozen Shipper", "Ice/Cold Pack", "Ambient", "Not Reported", "Other"]

ShipmentQuality = Literal["Normal", "Damaged", "Leakage", "Opened"]


CTCAEEventTerm = Annotated[str, AfterValidator(is_ctcae_event_term)]
CTCAEEventCode = Annotated[str, AfterValidator(is_ctcae_event_code)]


SeverityGradeSystem = Literal["CTCAE"]
SeverityGradeSystemVersionCTCAE = Literal["5.0", "6.0"]
SeverityGradeSystemVersion = SeverityGradeSystemVersionCTCAE


SeverityGradeCTCAE = Annotated[str, AfterValidator(is_ctcae_severity_grade)]
SeverityGrade = SeverityGradeCTCAE


SystemOrganClassCTCAE = Annotated[str, AfterValidator(is_ctcae_system_organ_class)]
SystemOrganClass = SystemOrganClassCTCAE


AttributionCause = Literal["Protocol as a whole", "Individual treatment"]
AttributionLikelihood = Literal["Unrelated", "Unlikely", "Possible", "Probable", "Definite", "Unknown"]


ECOGScore = Literal["0", "1", "2", "3", "4", "5"]
KarnofskyScore = Literal["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]


ExposureType = Literal[
    "Asbestos Exposure",
    "Chemical Exposure",
    "Marijuana Smoke Exposure",
    "Radiation Exposure",
    "Radon Exposure",
    "Respirable Crystalline Silica Exposure",
    "Smoke Exposure",
    "Smokeless Tobacco Exposure",
    "Tobacco Related Exposure",
    "Wood Dust Exposure",
]


TobaccoSmokingStatus = Literal[
    "Current smoker",
    "Former Smoker",
    "Never Smoker",
    "Unknown",
    "Not reported",
]


MalignancyStatus = Literal[
    "Active",
    "Partial remission",
    "Complete remission",
    "Recurrent/Relapsed",
    "Unknown",
]


ICD10CMCode = Annotated[str, AfterValidator(is_ICD10CM_code)]
ICD10CMTerm = Annotated[str, AfterValidator(is_ICD10CM_term)]


GVHDDiagnosisAcuteAssessmentSystem = Literal[
    "Modified Glucksberg",
    "MAGIC",
]

GVHDDiagnosisAcuteAssessmentSystemVersionModifiedGlucksberg = Literal["10.1038/s41409-018-0204-7"]

GVHDDiagnosisAcuteAssessmentSystemVersionMagic = Literal["10.1038/s41409-018-0204-7"]
GVHDDiagnosisAcuteAssessmentSystemVersion = (
    GVHDDiagnosisAcuteAssessmentSystemVersionModifiedGlucksberg | GVHDDiagnosisAcuteAssessmentSystemVersionMagic
)

GVHDDiagnosisAcuteGradeModifiedGlucksberg = Literal["0", "I", "II", "III", "IV"]
GVHDDiagnosisAcuteGradeMagic = Literal["0", "I", "II", "III", "IV"]
GVHDDiagnosisAcuteGrade = GVHDDiagnosisAcuteGradeModifiedGlucksberg | GVHDDiagnosisAcuteGradeMagic


PreOrPostEnrollment = Literal["Pre-enrollment", "Post-enrollment"]


GVHDOrgan = Annotated[str, AfterValidator(is_gvhd_organ)]

# They use the same stage PVs but we're explicit here to accommodate changes
GVHDOrganAcuteStageModifiedGlucksberg = Literal["0", "1", "2", "3", "4"]
GVHDOrganAcuteStageMagic = Literal["0", "1", "2", "3", "4"]
GVHDOrganAcuteStage = GVHDOrganAcuteStageModifiedGlucksberg | GVHDOrganAcuteStageMagic


GVHDDiagnosisChronicAssessmentSystem = Literal["NIH Consensus Criteria"]
GVHDDiagnosisChronicAssessmentSystemVersion = Literal["10.1016/j.bbmt.2014.12.001"]
GVHDDiagnosisChronicGlobalSeverity = Literal["Mild", "Moderate", "Severe"]


GVHDOrganChronicScore = Literal["0", "1", "2", "3"]


PriorTreatmentType = Literal[
    "Surgery",
    "Radiotherapy",
    "Immunotherapy",
    "Chemotherapy",
    "Targeted therapy",
    "Other therapy",
    "Radiopharmaceutical",
    "Stem cell transplant",
    "Immunosuppressive therapy/GVHD prophylaxis for transplant",
    "Conditioning therapy",
    "Post-transplant salvage therapy",
]


ConditioningRegimenType = Literal["Myeloablative", "Reduced-intensity", "Non-myeloablative", "Other"]

StemCellDonorType = Literal["Autologous", "Allogeneic"]


OffTreatmentReason = Literal[
    "Completion of Follow-Up",
    "Completion of Planned Therapy",
    "Death",
    "Disease Progression",
    "Failure to Attain Remission",
    "Ineligible",
    "Lost to Follow-Up",
    "Not Reported",
    "Other",
    "Physician Decision",
    "Relapse",
    "Secondary Malignancy",
    "Study Discontinuation",
    "Subject Non-Compliance",
    "Subject/Guardian Refused Further Treatment",
    "Toxicity",
    "Unknown",
    "Withdrawal of Consent",
]


TherapyAgentDoseUnits = Literal[
    "%",
    "10^8 IFU/mL",
    "10^9 IFU/mL",
    "10E10 Cell/kg",
    "10E10 Cells",
    "10E10 Viral Particles",
    "10E11 Cells",
    "10E11 Cells/kg",
    "10E11 Viral Particles",
    "10E13 Viral Particles",
    "10E3 Cell/kg",
    "10E3 Cells",
    "10E3 Cells/kg",
    "10E3 IU/kg",
    "10E4 Cell/kg",
    "10E4 Cells",
    "10E5 Cell/kg",
    "10E5 Cells",
    "10E6 Cell/kg",
    "10E6 Cells",
    "10E6 PFU",
    "10E7 Cell/kg",
    "10E7 Cells",
    "10E7 PFU",
    "10E8 Cell/kg",
    "10E8 Cells",
    "10E8 PFU",
    "10E9 Cell/kg",
    "10E9 Cells",
    "10E9 IU/mL",
    "10E9 PFU",
    "Ampule",
    "Applcatn",
    "au",
    "AUC",
    "bill PFU",
    "Bottle",
    "BPM",
    "Capful",
    "Caplet",
    "Capsule",
    "Cells",
    "Cells/kg",
    "cGy",
    "Ci",
    "Course",
    "Course",
    "Degree Celsius",
    "dL",
    "Dose",
    "E+10 Cells",
    "E+11 Cells",
    "E+3 Cells",
    "E+4 Cells",
    "E+5 Cells",
    "E+6 Cells",
    "E+7 Cells",
    "E+8 Cells",
    "E+9 Cells",
    "Eq",
    "g",
    "g/m2",
    "Gallon",
    "gtts",
    "Gy",
    "Hz",
    "Inch",
    "Inhalatn",
    "IU Vit A",
    "IU/mg",
    "IU/mg A-TE",
    "IUnit",
    "IUnit/kg",
    "IUnit/L",
    "IV Bag",
    "IVRP",
    "Jcm2",
    "KeV",
    "kg",
    "kHz",
    "kPa",
    "kU",
    "kU/kg",
    "kU/L",
    "L",
    "L/h/mg",
    "L/min",
    "mBq",
    "MBq",
    "mcg",
    "mcg/24h",
    "mcg/cm2",
    "mcg/hr",
    "mcg/kg",
    "mcg/m2",
    "mcg/min",
    "mCi",
    "Measure",
    "mEq",
    "mEq/24hr",
    "mEq/dL",
    "mEq/hr",
    "mEq/L",
    "MeV",
    "mg",
    "mg/24hr",
    "mg/dL",
    "mg/hr",
    "mg/inh",
    "mg/kg",
    "mg/kg/day",
    "mg/m2",
    "mg/mL",
    "mg/unit",
    "mg/wk",
    "MHz",
    "microCi",
    "microL",
    "micromol",
    "mill PFU",
    "Million",
    "millunit",
    "miu",
    "miu/m2",
    "mL",
    "mL",
    "mL/hr",
    "mL/kg",
    "mM/L",
    "mmol",
    "Mole",
    "mosmol",
    "Mrad",
    "MU",
    "mV",
    "MVP",
    "nCi",
    "ng",
    "ng/kg",
    "ng/L",
    "ng/mL",
    "nm light",
    "nmol",
    "No Srce",
    "osmol",
    "Other",
    "oz",
    "Pa",
    "packet",
    "Patch",
    "PFU",
    "pg",
    "psi",
    "puff",
    "Rad",
    "RAE",
    "RE",
    "Seed",
    "Session",
    "Spray",
    "Suppstry",
    "Sv",
    "Tablet",
    "Tbsp",
    "TCID",
    "Thousand",
    "Troche",
    "tsp",
    "uCi/kg",
    "umol/L/min",
    "Unit",
    "Unit/g",
    "Unit/kg",
    "Unit/m2",
    "Unit/mcg",
    "Unit/mL",
    "Unknown",
    "VP",
    "YU",
]


RadiotherapyProcedure = Literal[
    "3-Dimensional Conformal Radiation Therapy",
    "Brachytherapy",
    "Conventional Radiotherapy",
    "Electron Beam Radiation Therapy",
    "External Beam Radiation Therapy",
    "High-Dose Rate Brachytherapy",
    "Intensity-Modulated Radiation Therapy",
    "Low-Dose Rate Brachytherapy",
    "Not Reported",
    "Photon Beam Radiation Therapy",
    "Proton Beam Radiation Therapy",
    "Radiation Therapy",
    "Stereotactic Body Radiation Therapy",
    "Stereotactic Radiosurgery",
    "Unknown",
]

SurgicalProcedure = Literal[
    "Amputation",
    "Appendectomy",
    "Arterial Embolization",
    "Aspiration",
    "Bilateral Salpingo-oophorectomy (BSO)",
    "Bilobectomy",
    "Biopsy",
    "Cervical conization",
    "Chest wall resection",
    "Colectomy",
    "Continent Catheterizable Diversion",
    "Core biopsy",
    "Cryosurgery",
    "Cystoprostatectomy",
    "Deep lymphadenectomy",
    "Diaphram stripping",
    "Distal Pancreatectomy",
    "Endoscopic",
    "Esophagectomy",
    "EUA-bronchoscopy",
    "EUA-esophagoscopy",
    "EUA-laryngoscopy",
    "EUA-nasal endoscopy",
    "Excisional biopsy",
    "Exenteration",
    "Exploration",
    "Extrapulmonary Metastasis Resection",
    "Fine Needle Aspiration under CT Guidance",
    "Gastric Venting Tube",
    "Gross total resection with neck dissection",
    "Gross total resection without neck dissection",
    "Hemi vulvectomy",
    "Interval debulking",
    "Intracardial pneumonectomy",
    "Laparoscopic/Thoracoscopic",
    "Laparotomy",
    "Large Bowel resection",
    "Lobectomy",
    "Lung Segmentectomy",
    "Lymphadenectomy",
    "Mastectomy NOS",
    "Mediastinoscopy",
    "Mediastinotomy (Chamberlain procedure)",
    "Metastasectomy ",
    "Modified Radical Mastectomy",
    "Modified radical mastectomy after partial mastectomy as first attempt",
    "Modified radical neck dissection",
    "Neck Dissection",
    "Neck dissection level 1 to 4",
    "Neck dissection level 2 to 4",
    "Neobladder",
    "Nipple-Sparing Mastectomy",
    "Omentectomy",
    "Oncoplastic Partial Mastectomy/Lumpectomy with Oncoplastic Closure",
    "Open",
    "Other, specify",
    "Pancreatectomy",
    "Paraaortic lymph node sampling/dissection",
    "Partial Colectomy",
    "Partial Cystectomy",
    "Partial Hysterectomy",
    "Partial Mastectomy (Lumpectomy)",
    "Partial mastectomy with re-excision",
    "Partial mastectomy without re-excision",
    "Partial mastectomy/lumpectomy/excisional biopsy",
    "Partial Nephrectomy",
    "Partial Thyroidectomy",
    "Pelvic lymphadenectomy",
    "Pelvic node sampling",
    "Percutaneous",
    "Peritoneal  Sampling",
    "Peritoneal catheter insertion",
    "Peritonectomy  / Peritoneal stripping",
    "Pneumonectomy",
    "Primary debulking",
    "Prostatectomy",
    "Quadrantectomy",
    "Radical Cystectomy",
    "Radical Hysterectomy",
    "Radical Mastectomy",
    "Radical Nephrectomy",
    "Radical Trachelectomy",
    "Radical vulvectomy",
    "Re-excision",
    "Reassessment laparotomy",
    "Resection with reconstruction",
    "Resection without reconstruction",
    "Rotationplasty",
    "Segmentectomy",
    "Sentinel Lymph Node Biopsy",
    "Sentinel Lymph Node Mapping And Pelvic Lymphadenectomy",
    "Simple Nephrectomy",
    "Skin-sparing mastectomy",
    "Sleeve lobectomy",
    "Small Bowel resection",
    "Splenectomy",
    "Stent",
    "Stereotactic Biopsy",
    "Sternotomy",
    "Sublobar segmentectomy",
    "Superficial lymphadenectomy",
    "Surgical resection",
    "Thoracoabdominal  Esophagectomy",
    "Thoracoscopy",
    "Thoracotomy",
    "Thyroidectomy",
    "TORS deep tonsil biopsy",
    "TORS lingual tonsillectomy",
    "TORS palatine tonsillectomy",
    "TORS radical tonsillectomy",
    "Total Abdominal Hysterectomy",
    "Total Abdominal Hysterectomy with Bilateral Salpingo-Oophorectomy",
    "Total Hysterectomy",
    "Total Mastectomy",
    "Total Mesorectal Excision",
    "Total Pancreatectomy",
    "Total Vaginal Hysterectomy",
    "Tracheotomy",
    "Transanal Endoscopic",
    "Transbronchial needle biopsy (TBNA)",
    "Transurethral Resection",
    "Transurethral resection of bladder tumor (TURBT)",
    "Unilateral Salpingo-oophorectomy",
    "Vein Resection",
    "Wedge Resection",
    "Whipple",
]


RadiotherapyDoseUnits = Literal[
    "%",
    "CGE",
    "cGY",
    "Gy",
    "IU",
    "IU/m2",
    "mg",
    "mg/kg",
    "mg/m2",
    "mL",
    "Not Reported",
    "oz",
    "Unknown",
]


RadiationExtent = Literal["Extensive Radiation", "Limited Radiation", "Radiation, NOS"]


AllogeneicDonorType = Literal[
    "Haploidentical",
    "Matched related",
    "Matched unrelated",
    "Mismatched related",
    "Mismatched unrelated",
    "Syngeneic",
]


StemCellSource = Literal[
    "Peripheral blood",
    "Bone marrow",
    "Umbilical cord blood",
    "Unknown",
    "Other",
]
