import { generateFieldProps } from "./props_generator";

export const generateVocabularyFieldProps = (
  fieldName,
  fieldSchema,
  parentField,
  isCreate,
  formFieldConfig,
  formikProps,
  formFieldsConfig
) => {
  const fieldProps = generateFieldProps(
    fieldName,
    fieldSchema,
    parentField,
    isCreate,
    formFieldConfig,
    formikProps
  );
  const { vocabularyFieldProps } = {
    autocompleteFrom: `/api/vocabularies/${fieldSchema.metadata.type}`,
  };
  return { ...fieldProps, ...vocabularyFieldProps };
};
