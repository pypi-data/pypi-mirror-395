import { generateFieldProps } from "./props_generator";

export const generateDropdownFieldProps = (
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
  const arrayFieldProps = {
    defaultValue: formFieldConfig.dump_default,
  };
  return { ...fieldProps, ...arrayFieldProps };
};
