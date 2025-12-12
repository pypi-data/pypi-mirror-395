from typing import Self, Annotated, List

from pydantic import PositiveInt, NonNegativeFloat, PositiveFloat, model_validator, field_validator, BeforeValidator

from .base import Base
from cidc_api.models.types import (
    Sex,
    Race,
    Ethnicity,
    HeightUnits,
    WeightUnits,
    BodySurfaceAreaUnits,
    Occupation,
    Education,
    AgeAtEnrollmentUnits,
)


class Demographic(Base):
    __data_category__ = "demographic"
    __cardinality__ = "one"

    # The unique internal identifier for this demographic record
    demographic_id: int | None = None

    # The unique internal identifier for the associated participant
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12220014%20and%20ver_nr=1
    participant_id: str | None = None

    # The age of the subject when the subject enrolled in the study.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15742605%20and%20ver_nr=1
    age_at_enrollment: PositiveInt | None = None

    # Unit of measurement for the age of the participant. e.g. "Years"
    age_at_enrollment_units: AgeAtEnrollmentUnits | None = None

    # Indicates whether the participant is 90 years old or over. (for PHI purposes)
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15354920%20and%20ver_nr=1
    age_90_or_over: bool

    # A textual description of a person's sex at birth. e.g. "Male"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=7572817%20and%20ver_nr=3
    sex: Sex

    # The race of the participant. e.g. "White"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2192199%20and%20ver_nr=1
    race: Annotated[List[Race], BeforeValidator(Base.split_list)]

    # The ethnicity of the participant. e.g. "Hispanic or Latino"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2192217%20and%20ver_nr=2
    ethnicity: Ethnicity

    # The number that describes the vertical distance of the participant at enrollment date.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2179643%20and%20ver_nr=4
    height: PositiveFloat

    # Unit of measurement for the height of the participant at the enrollment date. e.g. "in"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2538920%20and%20ver_nr=1
    height_units: HeightUnits

    # The mass of the participant's entire body at the enrollment date.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2179689%20and%20ver_nr=4
    weight: PositiveFloat

    # Unit of measurement for the weight of the participant at the enrollment date. e.g. "kg"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2630200%20and%20ver_nr=1
    weight_units: WeightUnits

    # The body mass index of the participant at the enrollment date.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2006410%20and%20ver_nr=3
    body_mass_index: PositiveFloat

    # A decimal number that represents the measure of the 2-dimensional extent of the body surface (i.e., the skin) of the participant at the enrollment date.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6606197%20and%20ver_nr=1
    body_surface_area: PositiveFloat

    # Unit of measurement for body surface area of the participant at the enrollment date. e.g. "m2"
    # https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15114329%20and%20ver_nr=1
    body_surface_area_units: BodySurfaceAreaUnits

    # The occupation/job category of the participant. e.g. "Manager"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6617540%20and%20ver_nr=1
    occupation: Occupation | None = None

    # The amount of earnings in USD made by the participant's family in a year.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14834966%20and%20ver_nr=1
    income: NonNegativeFloat | None = None

    # The highest level of education attained by the participant. e.g. "Bachelor's Degree"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2681552%20and%20ver_nr=1
    highest_level_of_education: Education | None = None

    @model_validator(mode="after")
    def validate_age_at_enrollment_cr(self) -> Self:
        if self.age_90_or_over:
            if self.age_at_enrollment or self.age_at_enrollment_units:
                raise ValueError(
                    'If "age_90_or_over" is "Yes" then "age_at_enrollment" and "age_at_enrollment_units" must be blank.'
                )
        else:
            if not self.age_at_enrollment or not self.age_at_enrollment_units:
                raise ValueError(
                    'If "age_90_or_over" is "No" then "age_at_enrollment" and "age_at_enrollment_units" are required.'
                )
        return self

    @model_validator(mode="after")
    def validate_age_at_enrollment_value(self) -> Self:
        if not self.age_90_or_over:
            age_in_years = (
                self.age_at_enrollment if self.age_at_enrollment_units == "Years" else self.age_at_enrollment / 365.25
            )
            if age_in_years >= 90:
                raise ValueError('"age_at_enrollment" cannot represent a value greater than 90 years of age.')
        return self
