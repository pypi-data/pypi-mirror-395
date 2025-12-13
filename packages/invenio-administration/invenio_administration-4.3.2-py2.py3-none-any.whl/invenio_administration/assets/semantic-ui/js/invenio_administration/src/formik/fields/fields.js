import { generateObjectFieldProps, ObjectField } from "./object";
import { DynamicSubFormField, generateDynamicFieldProps } from "./dynamic";
import { generateHiddenFieldProps } from "./hidden";
import React from "react";
import {
  Input,
  AutocompleteDropdown,
  Dropdown,
  TextArea,
  RichInput,
} from "react-invenio-forms";
import { Field } from "formik";
import _get from "lodash/get";
import { AdminArrayField } from "./array";
import _isEmpty from "lodash/isEmpty";
import { sortFields } from "../../components/utils";
import { AdminBoolField, generateBoolFieldProps } from "./bool";
import { generateFieldProps } from "./props_generator";
import { generateVocabularyFieldProps } from "./vocabulary";
import { generateArrayFieldProps } from "./array";
import { generateDropdownFieldProps } from "./dropdown";

const fieldsMap = {
  string: { element: Input, props: generateFieldProps },
  integer: { element: Input, props: generateFieldProps },
  uuid: { element: Input, props: generateFieldProps },
  datetime: { element: Input, props: generateFieldProps },
  date: { element: Input, props: generateFieldProps },
  array: { element: AdminArrayField, props: generateArrayFieldProps },
  bool: { element: AdminBoolField, props: generateBoolFieldProps },
  hidden: { element: Field, props: generateHiddenFieldProps },
  vocabulary: { element: AutocompleteDropdown, props: generateVocabularyFieldProps },
  dynamic: { element: DynamicSubFormField, props: generateDynamicFieldProps },
  object: { element: ObjectField, props: generateObjectFieldProps },
  dropdown: { element: Dropdown, props: generateDropdownFieldProps },
  textarea: { element: TextArea, props: generateFieldProps },
  html: { element: RichInput, props: generateFieldProps },
  function: null,
};

export const mapFormFields = (
  obj,
  parentField,
  isCreate,
  formFieldsConfig,
  dropDumpOnly,
  formikProps,
  formData
) => {
  if (_isEmpty(obj)) {
    return <></>;
  }
  const sortedFields = sortFields(formFieldsConfig);
  const elements = Object.entries(sortedFields).map(([fieldName]) => {
    const fieldSchema = _get(obj, fieldName);
    const fieldConfig = formFieldsConfig[fieldName];

    if (fieldSchema.readOnly && dropDumpOnly) {
      return null;
    }

    let fieldType = fieldSchema.type;
    const isHidden = fieldSchema.metadata?.type === "hidden";

    if (isHidden) {
      fieldType = "hidden";
    }
    if (fieldSchema.type === "object" && fieldSchema.metadata?.type === "dynamic") {
      fieldType = "dynamic";
    }

    const options =
      fieldConfig?.options || fieldSchema?.metadata?.options || fieldSchema.enum;
    if (fieldSchema.type === "string" && options) {
      fieldType = "dropdown";
    }

    const rows = formFieldsConfig[fieldName]?.rows || fieldSchema?.metadata?.rows;
    if ((fieldSchema.type === "string" && rows) || fieldSchema.type === "dict") {
      fieldType = "textarea";
    }

    const Element = fieldsMap[fieldType].element;
    const fieldPropsGenerator = fieldsMap[fieldType].props;

    const fieldProps = fieldPropsGenerator(
      fieldName,
      fieldSchema,
      parentField,
      isCreate,
      fieldConfig,
      formikProps,
      formFieldsConfig,
      formData,
      mapFormFields
    );

    const showField =
      _isEmpty(formFieldsConfig) ||
      Object.prototype.hasOwnProperty.call(formFieldsConfig, fieldProps.name) ||
      Object.prototype.hasOwnProperty.call(
        formFieldsConfig,
        fieldProps.name.replace(`${parentField}.`, "")
      );

    if (!showField) {
      return null;
    }

    return <Element {...fieldProps} key={fieldProps.name} value={fieldProps.value} />;
  });

  return elements;
};
