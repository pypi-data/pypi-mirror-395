// This file is part of InvenioAdministration
// Copyright (C) 2022 CERN.
// Copyright (C) 2024 KTH Royal Institute of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import PropTypes from "prop-types";
import { Form, Formik } from "formik";
import { InvenioAdministrationActionsApi } from "../api/actions";
import { Button, Modal } from "semantic-ui-react";
import { Form as SemanticForm } from "semantic-ui-react";
import _get from "lodash/get";
import { ErrorMessage } from "../ui_messages";
import isEmpty from "lodash/isEmpty";
import { GenerateForm } from "./GenerateForm";
import { deserializeFieldErrors } from "../components/utils";
import { i18next } from "@translations/invenio_administration/i18next";
import Overridable from "react-overridable";

export class ActionFormLayout extends Component {
  render() {
    const {
      actionSchema,
      actionCancelCallback,
      actionConfig,
      formData,
      loading,
      error,
      onSubmit,
    } = this.props;
    return (
      <Formik initialValues={formData} onSubmit={onSubmit}>
        {(props) => (
          <>
            <Modal.Content>
              <SemanticForm as={Form} id="action-form" onSubmit={props.handleSubmit}>
                <GenerateForm
                  jsonSchema={actionSchema}
                  formFields={actionSchema}
                  create
                  dropDumpOnly
                  formikProps={props}
                  formData={formData}
                />
                {!isEmpty(error) && (
                  <ErrorMessage {...error} removeNotification={this.resetErrorState} />
                )}
              </SemanticForm>
            </Modal.Content>

            <Modal.Actions>
              <Button type="submit" primary form="action-form" loading={loading}>
                {i18next.t(actionConfig.text)}
              </Button>
              <Button
                onClick={actionCancelCallback}
                floated="left"
                icon="cancel"
                labelPosition="left"
                content={i18next.t("Cancel")}
              />
            </Modal.Actions>
          </>
        )}
      </Formik>
    );
  }
}

ActionFormLayout.propTypes = {
  actionSchema: PropTypes.object.isRequired,
  actionKey: PropTypes.string.isRequired,
  actionCancelCallback: PropTypes.func.isRequired,
  formFields: PropTypes.object,
  actionConfig: PropTypes.object.isRequired,
  actionPayload: PropTypes.object,
  error: PropTypes.object,
  formData: PropTypes.object,
  loading: PropTypes.bool,
  onSubmit: PropTypes.func.isRequired,
};

ActionFormLayout.defaultProps = {
  formFields: {},
  actionPayload: {},
  error: undefined,
  formData: undefined,
  loading: false,
};

class ActionForm extends Component {
  constructor(props) {
    super(props);
    const { actionPayload } = props;
    this.state = {
      loading: false,
      error: undefined,
      formData: actionPayload,
    };
  }

  onSubmit = async (formData, actions) => {
    this.setState({ loading: true });
    const { actionKey, actionSuccessCallback } = this.props;
    const actionEndpoint = this.getEndpoint(actionKey);

    const args = formData?.args;
    if (args) {
      formData.args = Object.fromEntries(
        Object.entries(args).map(([key, value]) => [key, value === "" ? null : value])
      );
    }

    try {
      const response = await InvenioAdministrationActionsApi.resourceAction(
        actionEndpoint,
        formData
      );
      this.setState({ loading: false });
      actionSuccessCallback(response.data);
    } catch (e) {
      console.error(e);
      this.setState({ loading: false });
      let errorMessage = e.message;

      // API errors need to be de-serialised to highlight fields.
      const apiResponse = e?.response?.data;
      if (apiResponse) {
        const apiErrors = apiResponse.errors || [];
        const deserializedErrors = deserializeFieldErrors(apiErrors);
        actions.setErrors(deserializedErrors);
        errorMessage = apiResponse.message || errorMessage;
      }

      this.setState({
        error: { header: i18next.t("Action error"), content: errorMessage, id: e.code },
      });
    }
  };

  getEndpoint = (actionKey) => {
    const { resource } = this.props;
    let endpoint;
    // get the action endpoint from the current resource links
    endpoint = _get(resource, `links.actions[${actionKey}]`);

    // endpoint can be also within links, not links.action
    // TODO: handle it in a nicer way
    if (isEmpty(endpoint)) {
      endpoint = _get(resource, `links[${actionKey}]`);
    }
    if (!endpoint) {
      console.error("Action endpoint not found in the resource!");
    }
    return endpoint;
  };

  resetErrorState = () => {
    this.setState({ error: undefined });
  };

  render() {
    const { actionSchema, actionCancelCallback, actionConfig, actionKey } = this.props;
    const { loading, formData, error } = this.state;
    return (
      <Overridable
        id={`InvenioAdministration.ActionForm.${actionKey}.layout`}
        loading={loading}
        formData={formData}
        error={error}
        {...this.props}
      >
        <ActionFormLayout
          actionSchema={actionSchema}
          actionCancelCallback={actionCancelCallback}
          actionConfig={actionConfig}
          actionKey={actionKey}
          loading={loading}
          formData={formData}
          error={error}
          onSubmit={this.onSubmit}
        />
      </Overridable>
    );
  }
}

ActionForm.propTypes = {
  resource: PropTypes.object.isRequired,
  actionSchema: PropTypes.object.isRequired,
  actionKey: PropTypes.string.isRequired,
  actionSuccessCallback: PropTypes.func.isRequired,
  actionCancelCallback: PropTypes.func.isRequired,
  formFields: PropTypes.object,
  actionConfig: PropTypes.object.isRequired,
  actionPayload: PropTypes.object,
};

ActionForm.defaultProps = {
  formFields: {},
  actionPayload: {},
};

export default Overridable.component("InvenioAdministration.ActionForm", ActionForm);
