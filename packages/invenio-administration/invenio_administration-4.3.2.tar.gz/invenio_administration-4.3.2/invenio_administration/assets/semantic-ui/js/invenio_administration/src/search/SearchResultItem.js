/*
 * This file is part of Invenio.
 * Copyright (C) 2022 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import PropTypes from "prop-types";
import React, { Component } from "react";
import { Table, Button } from "semantic-ui-react";
import isEmpty from "lodash/isEmpty";
import { Actions } from "../actions/Actions";
import { withState } from "react-searchkit";
import { AdminUIRoutes } from "../routes";
import Formatter from "../components/Formatter";
import Overridable from "react-overridable";

class SearchResultItemComponent extends Component {
  refreshAfterAction = () => {
    const { updateQueryState, currentQueryState } = this.props;
    updateQueryState(currentQueryState);
  };

  render() {
    const {
      title,
      resourceName,
      result,
      columns,
      displayEdit,
      displayDelete,
      actions,
      idKeyPath,
      resourceSchema,
      listUIEndpoint,
    } = this.props;

    const resourceHasActions = displayEdit || displayDelete || !isEmpty(actions);

    return (
      <Overridable
        id="InvenioAdministration.SearchResultItem.layout"
        title={title}
        resourceName={resourceName}
        result={result}
        columns={columns}
        displayEdit={displayEdit}
        displayDelete={displayDelete}
        actions={actions}
        idKeyPath={idKeyPath}
        resourceSchema={resourceSchema}
        listUIEndpoint={listUIEndpoint}
        resourceHasActions={resourceHasActions}
      >
        <Table.Row>
          {columns.map(([property, { text, order }], index) => {
            return (
              <Table.Cell
                key={`${text}-${order}`}
                data-label={text}
                className="word-break-all"
              >
                {index === 0 && (
                  <a
                    href={AdminUIRoutes.detailsView(listUIEndpoint, result, idKeyPath)}
                  >
                    <Formatter
                      result={result}
                      resourceSchema={resourceSchema}
                      property={property}
                    />
                  </a>
                )}
                {index !== 0 && (
                  <Formatter
                    result={result}
                    resourceSchema={resourceSchema}
                    property={property}
                  />
                )}
              </Table.Cell>
            );
          })}
          {resourceHasActions && (
            <Table.Cell collapsing>
              <Overridable id="InvenioAdministration.SearchResultItem.actions.container">
                <Button.Group size="tiny" basic widths={5} compact className="margined">
                  <Actions
                    title={title}
                    resourceName={resourceName}
                    editUrl={AdminUIRoutes.editView(listUIEndpoint, result, idKeyPath)}
                    displayEdit={displayEdit}
                    displayDelete={displayDelete}
                    actions={actions}
                    resource={result}
                    idKeyPath={idKeyPath}
                    successCallback={this.refreshAfterAction}
                    listUIEndpoint={listUIEndpoint}
                  />
                </Button.Group>
              </Overridable>
            </Table.Cell>
          )}
        </Table.Row>
      </Overridable>
    );
  }
}

SearchResultItemComponent.propTypes = {
  title: PropTypes.string.isRequired,
  resourceName: PropTypes.string.isRequired,
  result: PropTypes.object.isRequired,
  columns: PropTypes.array.isRequired,
  displayDelete: PropTypes.bool,
  displayEdit: PropTypes.bool,
  actions: PropTypes.object,
  updateQueryState: PropTypes.func.isRequired,
  currentQueryState: PropTypes.object.isRequired,
  idKeyPath: PropTypes.string.isRequired,
  resourceSchema: PropTypes.object.isRequired,
  listUIEndpoint: PropTypes.string.isRequired,
};

SearchResultItemComponent.defaultProps = {
  displayDelete: true,
  displayEdit: true,
  actions: {},
};

export const SearchResultItem = withState(SearchResultItemComponent);
