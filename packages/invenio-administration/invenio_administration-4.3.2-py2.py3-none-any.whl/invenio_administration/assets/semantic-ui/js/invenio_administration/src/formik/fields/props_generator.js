import React from "react";
import _capitalize from "lodash/capitalize";

export const generateFieldProps = (
  fieldName,
  fieldSchema,
  parentField,
  isCreate,
  formFieldConfig,
  formikProps
) => {
  let currentFieldName;

  const fieldLabel = formFieldConfig?.text || fieldSchema?.title || fieldName;
  const placeholder =
    formFieldConfig?.placeholder || fieldSchema?.metadata?.placeholder;

  if (parentField) {
    currentFieldName = `${parentField}.${fieldName}`;
  } else {
    currentFieldName = fieldName;
  }

  const htmlDescription = (
    <>
      <p />
      <div
        dangerouslySetInnerHTML={{
          __html: formFieldConfig?.description || fieldSchema?.metadata?.description,
        }}
      />
    </>
  );

  let dropdownOptions;
  dropdownOptions = formFieldConfig?.options || fieldSchema?.metadata?.options;

  if (!dropdownOptions && fieldSchema.enum) {
    dropdownOptions = fieldSchema.enum.map((value) => ({
      title_l10n: value,
      id: value,
    }));
  }

  return {
    fieldPath: currentFieldName,
    key: currentFieldName,
    label: _capitalize(fieldLabel),
    description: htmlDescription,
    required: fieldSchema.required,
    disabled: fieldSchema.readOnly || (fieldSchema.createOnly && !isCreate),
    placeholder,
    options: dropdownOptions,
    rows: formFieldConfig?.rows || fieldSchema?.metadata?.rows,
    value: formFieldConfig.dump_default,
    name: currentFieldName,
  };
};
