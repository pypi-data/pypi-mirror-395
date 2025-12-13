# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def post_init_hook(cr, registry):
    cr.execute(
        """
    UPDATE
        hr_employee dest
    SET
        manual_salary_structure_id = src.salary_structure_id
    FROM hr_employee src
    WHERE
        dest.id = src.id;
    """
    )
