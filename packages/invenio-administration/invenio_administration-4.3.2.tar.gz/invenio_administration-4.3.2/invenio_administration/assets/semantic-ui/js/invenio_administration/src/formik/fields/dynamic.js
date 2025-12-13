import { generateFieldProps } from "./props_generator";
import { LazyForm } from "../LazyForm";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { Form, Segment, Header } from "semantic-ui-react";

export const generateDynamicFieldProps = (
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
  const dynamicFieldProps = {
    formData: formData,
    formikProps: formikProps,
    fieldSchema: fieldSchema,
  };
  return { ...fieldProps, ...dynamicFieldProps };
};

export class DynamicSubFormField extends Component {
  render() {
    const { formikProps, fieldSchema, formData, ...fieldProps } = this.props;

    return (
      <React.Fragment key={fieldProps.name}>
        <Header attached="top" as="h5">
          {fieldProps.label}
        </Header>
        <Segment attached="bottom">
          <Form.Group grouped>
            <LazyForm
              {...fieldProps}
              formikProps={formikProps}
              fieldSchema={fieldSchema}
              key={fieldProps.name}
              formData={formData}
            />
          </Form.Group>
        </Segment>
      </React.Fragment>
    );
  }
}

DynamicSubFormField.propTypes = {
  fieldSchema: PropTypes.object.isRequired,
  formikProps: PropTypes.object.isRequired,
  formData: PropTypes.object.isRequired,
};
