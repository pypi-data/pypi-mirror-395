import { NotificationController } from "../ui_messages";
import { SearchResultsBulkActionsManager } from "react-invenio-forms";
import PropTypes from "prop-types";
import React, { Component } from "react";

export class SearchBulkActionContext extends Component {
  render() {
    const { children } = this.props;
    return (
      <NotificationController>
        <SearchResultsBulkActionsManager>{children}</SearchResultsBulkActionsManager>
      </NotificationController>
    );
  }
}

SearchBulkActionContext.propTypes = {
  children: PropTypes.node.isRequired,
};
