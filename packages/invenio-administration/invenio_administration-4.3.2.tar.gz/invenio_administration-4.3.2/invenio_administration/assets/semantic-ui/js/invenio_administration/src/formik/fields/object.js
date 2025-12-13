import { generateFieldProps } from "./props_generator";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { Form, Segment, Header } from "semantic-ui-react";

export const generateObjectFieldProps = (
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
  const objectFieldProps = {
    mapFormFields: mapFormFields,
    fieldSchema: fieldSchema,
  };
  return { ...fieldProps, ...objectFieldProps };
};

export class ObjectField extends Component {
  render() {
    const { mapFormFields, fieldSchema, isCreate, formFieldsConfig, ...fieldProps } =
      this.props;
    return (
      <React.Fragment key={fieldProps.name}>
        <Header attached="top" as="h5">
          {fieldProps.label}
        </Header>
        <Segment attached="bottom">
          <Form.Group grouped>
            {mapFormFields(
              fieldSchema.properties,
              fieldProps.name,
              isCreate,
              formFieldsConfig
            )}
          </Form.Group>
        </Segment>
      </React.Fragment>
    );
  }
}

ObjectField.propTypes = {
  fieldProps: PropTypes.object.isRequired,
  fieldSchema: PropTypes.object.isRequired,
  formFieldsConfig: PropTypes.object.isRequired,
  isCreate: PropTypes.bool,
  mapFormFields: PropTypes.func.isRequired,
};

ObjectField.defaultProps = {
  isCreate: false,
};
