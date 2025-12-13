from decimal import Decimal

import pytest

from snowflake.core.user_defined_function import Argument, ReturnDataType, SQLFunction, UserDefinedFunction
from tests.utils import random_string


@pytest.mark.min_sf_ver("9.38.0")
def test_execute_udf_decfloat(user_defined_functions, cursor):
    udf_name = random_string(10, "test_execute_udf_decfloat_")
    udf = UserDefinedFunction(
        name=udf_name,
        arguments=[Argument(name="arg", datatype="DECFLOAT")],
        return_type=ReturnDataType(datatype="DECFLOAT"),
        language_config=SQLFunction(),
        body="SELECT DECFLOAT '1.23e-2' + ARG",
    )

    udf_handle = user_defined_functions.create(udf)
    try:
        udf_fqn = f"{user_defined_functions.database.name}.{user_defined_functions.schema.name}.{udf_name}"
        # TODO: replace by execute method once we have it
        result = cursor.execute(f"SELECT {udf_fqn}(DECFLOAT '1.02')").fetchone()[0]
        assert result == Decimal("1.0323")
    finally:
        udf_handle.drop(if_exists=True)
