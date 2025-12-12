# ssb-datadoc-model

Data Model for use in Statistics Norway's Metadata system

## Purpose

This package contains pydantic models defining the fields and data types used in Statistics Norway's metadata system. The purpose of these models is to:

- Enable validation of user data
- Enable serialization and deserialization of metadata files
- Support versioning of the metadata format
- Enforce consistency across multiple tools

## Release

To release this package, create a branch and run `uv version --bump [patch | minor | major]` depending on your change. Once the branch is merged, a GitHub Actions workflow handles the rest.
