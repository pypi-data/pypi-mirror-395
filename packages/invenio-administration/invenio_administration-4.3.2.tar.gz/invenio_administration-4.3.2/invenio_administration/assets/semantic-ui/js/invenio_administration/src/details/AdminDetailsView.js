import { AdminUIRoutes } from "@js/invenio_administration/src/routes";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { Grid, Header, Divider, Container, Button } from "semantic-ui-react";
import { InvenioAdministrationActionsApi } from "../api/actions";
import DetailsTable from "./DetailsComponent";
import { Actions } from "../actions/Actions";
import _isEmpty from "lodash/isEmpty";
import { sortFields } from "../components/utils";
import { Loader, ErrorPage } from "../components";
import Overridable from "react-overridable";

class AdminDetailsView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: true,
      data: undefined,
      error: undefined,
    };
  }

  componentDidMount() {
    this.fetchData();
  }

  fetchData = async () => {
    this.setState({ loading: true });
    const { apiEndpoint, pid, requestHeaders } = this.props;
    try {
      const response = await InvenioAdministrationActionsApi.getResource(
        apiEndpoint,
        pid,
        requestHeaders
      );

      this.setState({
        loading: false,
        data: response.data,
        error: undefined,
      });
    } catch (e) {
      console.error(e);
      this.setState({ error: e, loading: false });
    }
  };

  childrenWithData = (data, columns) => {
    const { children } = this.props;
    return React.Children.map(children, (child) => {
      if (React.isValidElement(child)) {
        return React.cloneElement(child, { data: data, columns: columns });
      }
      return child;
    });
  };

  handleDelete = () => {
    // after deleting the resource go back to the list view
    const { listUIEndpoint } = this.props;
    window.location.href = listUIEndpoint;
  };

  render() {
    const {
      title,
      columns,
      actions,
      apiEndpoint,
      idKeyPath,
      listUIEndpoint,
      resourceSchema,
      resourceName,
      displayDelete,
      displayEdit,
      uiSchema,
      name,
    } = this.props;
    const { loading, data, error } = this.state;
    const sortedColumns = sortFields(uiSchema);
    return (
      <Overridable
        id={`InvenioAdministration.AdminDetailsView.${name}.layout`}
        data={data}
        error={error}
        loading={loading}
        {...this.props}
      >
        <Loader isLoading={loading}>
          <ErrorPage
            error={!_isEmpty(error)}
            errorCode={error?.response.status}
            errorMessage={error?.response.data}
          >
            <Grid stackable>
              <Grid.Row columns="2">
                <Grid.Column verticalAlign="middle">
                  <Header as="h1">{title}</Header>
                </Grid.Column>
                <Grid.Column verticalAlign="middle" floated="right" textAlign="right">
                  <Button.Group size="tiny" className="relaxed">
                    <Actions
                      title={title}
                      resourceName={resourceName}
                      apiEndpoint={apiEndpoint}
                      editUrl={AdminUIRoutes.editView(listUIEndpoint, data, idKeyPath)}
                      actions={actions}
                      displayEdit={displayEdit}
                      displayDelete={displayDelete}
                      resource={data}
                      idKeyPath={idKeyPath}
                      successCallback={this.handleDelete}
                      listUIEndpoint={listUIEndpoint}
                    />
                  </Button.Group>
                </Grid.Column>
              </Grid.Row>
            </Grid>
            <Divider />
            <Container fluid>
              <DetailsTable
                data={data}
                schema={resourceSchema}
                uiSchema={sortedColumns}
              />
              {this.childrenWithData(data, columns)}
            </Container>
          </ErrorPage>
        </Loader>
      </Overridable>
    );
  }
}

AdminDetailsView.propTypes = {
  actions: PropTypes.object,
  apiEndpoint: PropTypes.string.isRequired,
  columns: PropTypes.object.isRequired,
  displayEdit: PropTypes.bool.isRequired,
  displayDelete: PropTypes.bool.isRequired,
  pid: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  children: PropTypes.object,
  resourceName: PropTypes.string.isRequired,
  idKeyPath: PropTypes.string.isRequired,
  listUIEndpoint: PropTypes.string.isRequired,
  resourceSchema: PropTypes.object.isRequired,
  requestHeaders: PropTypes.object.isRequired,
  uiSchema: PropTypes.object.isRequired,
  name: PropTypes.string.isRequired,
};

AdminDetailsView.defaultProps = {
  actions: undefined,
  children: undefined,
};

export default Overridable.component(
  "InvenioAdministration.AdminDetailsView",
  AdminDetailsView
);
