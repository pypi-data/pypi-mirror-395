# -*- coding: utf-8 -*-
"""
tqwgp-parser.files.loaders
~~~~~~~~~~~~~~~~~~~~~
Files / projects loading facilities for the TQWGP parser.

:copyright: (c) 2022 Yoan Tournade.
"""
import os
import pathlib
import glob


def load_documents_from_project(
    project_specifier,
    default_projects_dir=None,
    default_document_path=None,
    throw_error=True,
):
    project_path = None
    project_name = None
    document_path = None
    if os.path.isdir(project_specifier):
        # This is directly the project directory.
        project_path = project_specifier
    elif os.path.isfile(project_specifier):
        # This is directly the document path.
        document_path = project_specifier
        project_path = os.path.dirname(document_path)
    elif default_projects_dir:
        # We should look in the default projects directory.
        project_name = project_specifier
        project_path = default_projects_dir
    if not project_path:
        error_str = "No project directory found for specified {}".format(
            project_specifier
        )
        if throw_error:
            raise ValueError(error_str)
        return "value_error", error_str, None, None
    if not document_path and default_document_path:
        # We should look for the default document path in
        # the project directory.
        document_path = os.path.join(project_path, default_document_path)
    documents_paths = glob.glob(document_path)
    if not documents_paths:
        error_str = "No document found for project path and specifier {}:{} (default path: {})".format(
            project_path,
            project_specifier,
            default_document_path,
        )
        if throw_error:
            raise ValueError(error_str)
        return "value_error", error_str, None, None
    project_path = os.path.realpath(project_path)
    # Extract project name.
    extracted_project_name = project_path.split("/")[
        -2 if project_path[-1] == "/" else -1
    ]
    if project_name and project_name != extracted_project_name:
        error_str = "Project names mismatched; provided: {}; extract: {}".format(
            project_name, extracted_project_name
        )
        if throw_error:
            raise ValueError(error_str)
        return "value_error", error_str, None, None
    returned_documents_paths = [
        os.path.realpath(document_path) for document_path in documents_paths
    ]
    if throw_error:
        return project_path, returned_documents_paths, extracted_project_name
    return "ok", project_path, returned_documents_paths, extracted_project_name


def load_document_with_inheritance(
    document_path, open_fn, parser_fn, inherit_parent_key="inherit"
):
    rec_n = 0
    current_document_path = document_path
    # Load the document hierarchy.
    document_contents = []
    while True:
        rec_n += 1
        if rec_n > 3:
            raise RuntimeError("Recursive loop")
        with open_fn(current_document_path) as f:
            content = f.read()
            parsed_current_document = parser_fn(content)
            document_contents.append(parsed_current_document)
            if not parsed_current_document.get(inherit_parent_key):
                break
            # Loads the parent document file, with a path
            # relative to the current document.
            current_document_path = (
                (
                    pathlib.Path(current_document_path).parent
                    / parsed_current_document[inherit_parent_key]
                )
                .resolve()
                .as_posix()
            )
    # Merge documents, by beginning by the parent.
    document_contents.reverse()
    consolidated_document = None
    for document_content in document_contents:
        if not consolidated_document:
            consolidated_document = document_content
            continue
        # We use a shallow merge for the moment:
        # only for top-level keys.
        consolidated_document = {
            **consolidated_document,
            **document_content,
        }
    return consolidated_document
