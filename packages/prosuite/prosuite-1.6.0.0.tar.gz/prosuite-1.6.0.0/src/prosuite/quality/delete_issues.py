from enum import IntEnum


class DeleteIssuesInVerifiedModel(IntEnum):
    delete_issues_in_perimeter_with_condition = 0
    delete_all_issues_in_perimeter  = 1
    delete_no_issues = 2
