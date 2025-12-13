import React from "react";
import PropTypes from "prop-types";
import { mapFormFields } from "./fields/fields";

export const GenerateForm = ({
  jsonSchema,
  create,
  formFields,
  dropDumpOnly,
  formikProps,
  parentField,
  formData,
}) => {
  const properties = jsonSchema;
  return (
    <>
      {mapFormFields(
        properties,
        parentField,
        create,
        formFields,
        dropDumpOnly,
        formikProps,
        formData
      )}
    </>
  );
};

GenerateForm.propTypes = {
  jsonSchema: PropTypes.object.isRequired,
  create: PropTypes.bool,
  formFields: PropTypes.object,
  dropDumpOnly: PropTypes.bool,
  formikProps: PropTypes.object,
  parentField: PropTypes.string,
  formData: PropTypes.object,
};

GenerateForm.defaultProps = {
  create: false,
  formFields: undefined,
  dropDumpOnly: false,
  parentField: undefined,
};
