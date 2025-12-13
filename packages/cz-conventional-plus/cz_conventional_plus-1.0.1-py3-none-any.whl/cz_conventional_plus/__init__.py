from commitizen.cz.conventional_commits.conventional_commits import \
    ConventionalCommitsCz
from commitizen.defaults import Questions


class ConventionalPlusCz(ConventionalCommitsCz):

    def questions(self) -> Questions:
        questions = super().questions()
        for q in questions:
            if q.get("name") == "prefix":
                q["choices"].extend(
                    (
                        dict(
                            value="chore",
                            name="chore: Other changes that don't modify src or test files",
                        ),
                        dict(value="revert", name="revert: Reverts a previous commit"),
                    )
                )
        return questions
