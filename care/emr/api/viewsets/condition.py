from django_filters import CharFilter, FilterSet, UUIDFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

from care.emr.api.viewsets.base import EMRModelViewSet
from care.emr.models.condition import Condition
from care.emr.registries.system_questionnaire.system_questionnaire import (
    InternalQuestionnaireRegistry,
)
from care.emr.resources.condition.spec import (
    CategoryChoices,
    ConditionSpec,
    ConditionSpecRead,
)
from care.emr.resources.questionnaire.spec import SubjectType
from care.facility.models.patient_consultation import PatientConsultation


class ConditionFilters(FilterSet):
    encounter = UUIDFilter(field_name="encounter__external_id")
    clinical_status = CharFilter(field_name="clinical_status", lookup_expr="iexact")
    verification_status = CharFilter(
        field_name="verification_status", lookup_expr="iexact"
    )
    severity = CharFilter(field_name="severity", lookup_expr="iexact")


class SymptomViewSet(EMRModelViewSet):
    database_model = Condition
    pydantic_model = ConditionSpec
    pydantic_read_model = ConditionSpecRead
    questionnaire_type = "symptom"
    questionnaire_title = "Symptom"
    questionnaire_description = "Symptom"
    questionnaire_subject_type = SubjectType.patient.value
    filterset_class = ConditionFilters
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, instance):
        instance.category = CategoryChoices.problem_list_item.value
        super().perform_create(instance)

    def authorize_create(self, request, request_model: ConditionSpec):
        encounter = PatientConsultation.objects.get(external_id=request_model.encounter)
        if str(encounter.patient.external_id) != self.kwargs["patient_external_id"]:
            err = "Malformed request"
            raise PermissionDenied(err)
        # Check if the user has access to the patient and write access to the encounter

    def get_queryset(self):
        # Check if the user has read access to the patient and their EMR Data
        return (
            super()
            .get_queryset()
            .filter(
                patient__external_id=self.kwargs["patient_external_id"],
                category=CategoryChoices.problem_list_item.value,
            )
            .select_related("patient", "encounter", "created_by", "updated_by")
        )


InternalQuestionnaireRegistry.register(SymptomViewSet)


class DiagnosisViewSet(EMRModelViewSet):
    database_model = Condition
    pydantic_model = ConditionSpec
    pydantic_read_model = ConditionSpecRead
    questionnaire_type = "diagnosis"
    questionnaire_title = "Diagnosis"
    questionnaire_description = "Diagnosis"
    questionnaire_subject_type = SubjectType.patient.value
    filterset_class = ConditionFilters
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, instance):
        instance.category = CategoryChoices.encounter_diagnosis.value
        super().perform_create(instance)

    def authorize_create(self, request, request_model: ConditionSpec):
        encounter = PatientConsultation.objects.get(external_id=request_model.encounter)
        if str(encounter.patient.external_id) != self.kwargs["patient_external_id"]:
            err = "Malformed request"
            raise PermissionDenied(err)
        # Check if the user has access to the patient and write access to the encounter

    def get_queryset(self):
        # Check if the user has read access to the patient and their EMR Data
        return (
            super()
            .get_queryset()
            .filter(
                patient__external_id=self.kwargs["patient_external_id"],
                category=CategoryChoices.encounter_diagnosis.value,
            )
            .select_related("patient", "encounter", "created_by", "updated_by")
        )


InternalQuestionnaireRegistry.register(DiagnosisViewSet)
