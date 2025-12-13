import os
from ara_cli.list_filter import ListFilter, filter_list
from ara_cli.artefact_models.artefact_data_retrieval import (
    artefact_content_retrieval,
    artefact_path_retrieval,
    artefact_tags_retrieval,
)

class TagExtractor:
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def filter_column(self, tag_groups, filtered_artefacts):
        status_tags = {"to-do", "in-progress", "review", "done", "closed"}

        artefacts_to_process = self._get_artefacts_without_status_tags(
            filtered_artefacts, status_tags
        )
        self._add_non_status_tags_to_set(tag_groups, artefacts_to_process, status_tags)

    def _get_artefacts_without_status_tags(self, filtered_artefacts, status_tags):
        artefacts_to_process = []
        for artefact_list in filtered_artefacts.values():
            for artefact in artefact_list:
                tag_set = self._get_tag_set(artefact)
                if not tag_set & status_tags:
                    artefacts_to_process.append(artefact)
        return artefacts_to_process

    def _get_tag_set(self, artefact):
        tags = artefact.tags + [artefact.status] if artefact.status else artefact.tags
        return set(tag for tag in tags if tag is not None)

    def _add_non_status_tags_to_set(self, tag_groups, artefacts, status_tags):
        for artefact in artefacts:
            tags = [
                tag for tag in (artefact.tags + [artefact.status]) if tag is not None
            ]
            for tag in tags:
                if self._is_skipped_tag(tag, status_tags):
                    continue
                key = tag.lower()
                if key not in tag_groups:
                    tag_groups[key] = set()
                tag_groups[key].add(tag)

    def _is_skipped_tag(self, tag, status_tags):
        return (
            tag in status_tags or tag.startswith("priority_") or tag.startswith("user_")
        )

    def _collect_all_tags(self, artefact):
        """Collect all tags from an artefact including user tags and author."""
        all_tags = []
        all_tags.extend(artefact.tags)
        
        if artefact.status:
            all_tags.append(artefact.status)
            
        user_tags = [f"user_{tag}" for tag in artefact.users]
        all_tags.extend(user_tags)
        
        if hasattr(artefact, 'author') and artefact.author:
            all_tags.append(artefact.author)
            
        return [tag for tag in all_tags if tag is not None]

    def _add_tags_to_groups(self, tag_groups, tags):
        """Add tags to tag groups."""
        for tag in tags:
            key = tag.lower()
            if key not in tag_groups:
                tag_groups[key] = set()
            tag_groups[key].add(tag)

    def add_to_tags_set(self, tag_groups, filtered_artefacts):
        for artefact_list in filtered_artefacts.values():
            for artefact in artefact_list:
                all_tags = self._collect_all_tags(artefact)
                self._add_tags_to_groups(tag_groups, all_tags)

    def extract_tags(
        self,
        navigate_to_target=False,
        filtered_extra_column=False,
        list_filter: ListFilter | None = None,
    ):
        from ara_cli.template_manager import DirectoryNavigator
        from ara_cli.artefact_reader import ArtefactReader

        navigator = DirectoryNavigator()
        if navigate_to_target:
            navigator.navigate_to_target()

        artefacts = ArtefactReader.read_artefacts()

        filtered_artefacts = filter_list(
            list_to_filter=artefacts,
            list_filter=list_filter,
            content_retrieval_strategy=artefact_content_retrieval,
            file_path_retrieval=artefact_path_retrieval,
            tag_retrieval=artefact_tags_retrieval,
        )

        tag_groups = {}

        if filtered_extra_column:
            self.filter_column(tag_groups, filtered_artefacts)
        else:
            self.add_to_tags_set(tag_groups, filtered_artefacts)

        return tag_groups