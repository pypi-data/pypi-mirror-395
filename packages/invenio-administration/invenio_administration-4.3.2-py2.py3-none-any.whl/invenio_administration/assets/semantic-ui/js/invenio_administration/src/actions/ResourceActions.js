import React, { Component } from "react";
import PropTypes from "prop-types";
import { Button, Modal, Icon } from "semantic-ui-react";
import { ActionForm } from "../formik";
import ActionModal from "./ActionModal";
import _isEmpty from "lodash/isEmpty";
import Overridable from "react-overridable";

class ResourceActions extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modalOpen: false,
      modalHeader: undefined,
      modalBody: undefined,
    };
  }

  onModalTriggerClick = (e, { payloadSchema, dataName, dataActionKey }) => {
    const { resource, actions: actionsConfig } = this.props;
    this.setState({
      modalOpen: true,
      modalHeader: dataName,
      modalBody: (
        <Overridable
          id={`InvenioAdministration.ResourceActions.ModalBody.${dataActionKey}`}
          actionKey={dataActionKey}
          actionSchema={payloadSchema}
          actionSuccessCallback={this.onModalClose}
          actionCancelCallback={this.closeModal}
          resource={resource}
          actionConfig={actionsConfig[dataActionKey]}
        >
          <ActionForm
            actionKey={dataActionKey}
            actionSchema={payloadSchema}
            actionSuccessCallback={this.onModalClose}
            actionCancelCallback={this.closeModal}
            resource={resource}
            actionConfig={actionsConfig[dataActionKey]}
          />
        </Overridable>
      ),
    });
  };

  closeModal = () => {
    this.setState({
      modalOpen: false,
      modalHeader: undefined,
      modalBody: undefined,
    });
  };

  onModalClose = () => {
    const { successCallback } = this.props;
    this.setState({
      modalOpen: false,
      modalHeader: undefined,
      modalBody: undefined,
    });
    successCallback();
  };

  render() {
    const { actions, Element, resource } = this.props;
    const { modalOpen, modalHeader, modalBody } = this.state;
    return (
      <>
        {Object.entries(actions).map(([actionKey, actionConfig]) => {
          const icon = actionConfig.icon;
          const labelPos = icon ? "left" : null;
          return (
            <Element
              key={actionKey}
              onClick={this.onModalTriggerClick}
              payloadSchema={actionConfig.payload_schema}
              dataName={actionConfig.text}
              dataActionKey={actionKey}
              basic
              icon={!_isEmpty(icon)}
              labelPosition={labelPos}
            >
              {!_isEmpty(icon) && <Icon name={icon} />}
              {actionConfig.text}...
            </Element>
          );
        })}
        <ActionModal modalOpen={modalOpen} resource={resource}>
          {modalHeader && <Modal.Header>{modalHeader}</Modal.Header>}
          {!_isEmpty(modalBody) && modalBody}
        </ActionModal>
      </>
    );
  }
}

ResourceActions.propTypes = {
  resource: PropTypes.object.isRequired,
  successCallback: PropTypes.func.isRequired,
  actions: PropTypes.object.isRequired,
  Element: PropTypes.node,
};

ResourceActions.defaultProps = {
  Element: Button,
};

export default Overridable.component(
  "InvenioAdministration.ResourceActions",
  ResourceActions
);
