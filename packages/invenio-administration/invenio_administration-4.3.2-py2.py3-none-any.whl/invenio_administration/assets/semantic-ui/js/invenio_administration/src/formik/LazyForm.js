import { InvenioAdministrationActionsApi } from "@js/invenio_administration/src/api";
import { GenerateForm } from "@js/invenio_administration/src/formik/GenerateForm";
import isEmpty from "lodash/isEmpty";
import React, { Component } from "react";
import PropTypes from "prop-types";
import { getIn } from "formik";

export class LazyForm extends Component {
  constructor(props) {
    super(props);
    const { fieldSchema } = props;
    this.state = {
      lazySchema: {},
      fieldSchema: fieldSchema,
    };
  }

  handleFieldValueChange = async (value) => {
    const { fieldSchema } = this.state;
    const { formikProps, fieldPath } = this.props;
    const { endpoint } = fieldSchema.metadata;
    try {
      const response = await InvenioAdministrationActionsApi.getSchema(endpoint, value);
      fieldSchema["properties"] = response.data;
      this.setState({ lazySchema: response.data, fieldSchema: { ...fieldSchema } });
      for (const [key, value] of Object.entries(response.data)) {
        formikProps.setFieldValue(`${fieldPath}.${key}`, value.load_default);
      }
    } catch (e) {
      console.error(e);
    }
  };

  componentDidUpdate(prevProps, prevState, snapshot) {
    const { formikProps } = this.props;
    const { fieldSchema } = this.state;
    const { depends_on: dependsOnField } = fieldSchema.metadata;
    const previousValue = getIn(prevProps.formikProps.values, dependsOnField, "");
    const choiceValue = getIn(formikProps.values, dependsOnField, "");
    if (previousValue !== choiceValue) {
      this.handleFieldValueChange(choiceValue);
    }
  }

  componentDidMount() {
    const { formikProps, fieldSchema, fieldPath, formData } = this.props;
    const { depends_on: dependsOnField } = fieldSchema.metadata;
    const choiceValue = getIn(formikProps.values, dependsOnField, "");
    if (!isEmpty(choiceValue)) {
      this.handleFieldValueChange(choiceValue);
    }
  }

  render() {
    const { formikProps, fieldPath } = this.props;
    const { lazySchema } = this.state;
    if (isEmpty(lazySchema)) {
      return null;
    }
    return (
      <GenerateForm
        jsonSchema={lazySchema}
        formFields={lazySchema}
        parentField={fieldPath}
        formikProps={formikProps}
        create
        dropDumpOnly
      />
    );
  }
}

LazyForm.propTypes = {
  formikProps: PropTypes.object.isRequired,
  fieldSchema: PropTypes.object.isRequired,
  fieldPath: PropTypes.string.isRequired,
  formData: PropTypes.object,
};
