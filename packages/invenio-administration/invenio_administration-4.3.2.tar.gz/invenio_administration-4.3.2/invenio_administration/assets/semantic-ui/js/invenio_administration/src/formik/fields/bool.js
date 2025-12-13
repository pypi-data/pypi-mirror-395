import { generateFieldProps } from "./props_generator";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { BooleanField } from "react-invenio-forms";

export const generateBoolFieldProps = (
  fieldName,
  fieldSchema,
  parentField,
  isCreate,
  formFieldConfig,
  formikProps,
  formFieldsConfig,
  formData
) => {
  const fieldProps = generateFieldProps(
    fieldName,
    fieldSchema,
    parentField,
    isCreate,
    formFieldConfig,
    formikProps
  );
  const boolFieldProps = {
    fieldSchema: fieldSchema,
  };
  return { ...fieldProps, ...boolFieldProps };
};

export class AdminBoolField extends Component {
  render() {
    const { fieldSchema, ...fieldProps } = this.props;
    const description = fieldProps.description;

    return (
      <>
        <BooleanField
          key={fieldProps.name}
          required={fieldSchema.required}
          value={fieldSchema.metadata.checked === "true"}
          {...fieldProps}
        />
        {description && <label className="helptext">{description}</label>}
      </>
    );
  }
}

AdminBoolField.propTypes = {
  fieldProps: PropTypes.object.isRequired,
  fieldSchema: PropTypes.object.isRequired,
};
