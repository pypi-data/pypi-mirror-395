import { generateFieldProps } from "./props_generator";
import React, { Component } from "react";
import PropTypes from "prop-types";

export const generateHiddenFieldProps = (
  fieldName,
  fieldSchema,
  parentField,
  isCreate,
  formFieldConfig,
  formikProps,
  formFieldsConfig,
  formData,
  mapFormFields
) => {
  const fieldProps = generateFieldProps(
    fieldName,
    fieldSchema,
    parentField,
    isCreate,
    formFieldConfig,
    formikProps
  );
  return { ...fieldProps, type: "hidden", name: fieldProps.name };
};
