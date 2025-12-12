# Copyright (c) 2024 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: errors.j2

# pylint: disable=duplicate-code
# pylint: disable=line-too-long
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-statements
# pylint: disable=unused-import

# AccelByte Gaming Services Leaderboard Service

from accelbyte_py_sdk.core import ApiError

ERROR_20000 = ApiError(code="20000", message="internal server error")
ERROR_20001 = ApiError(code="20001", message="unauthorized access")
ERROR_20002 = ApiError(code="20002", message="validation error")
ERROR_20013 = ApiError(code="20013", message="insufficient permissions")
ERROR_20019 = ApiError(code="20019", message="unable to parse request body")
ERROR_71130 = ApiError(code="71130", message="leaderboard config not found")
ERROR_71132 = ApiError(code="71132", message="leaderboard configuration already exist")
ERROR_71133 = ApiError(code="71133", message="leaderboard configuration deleted")
ERROR_71230 = ApiError(code="71230", message="leaderboard configuration not found")
ERROR_71233 = ApiError(code="71233", message="user ranking data not found")
ERROR_71235 = ApiError(code="71235", message="leaderboard ranking not found")
ERROR_71236 = ApiError(code="71236", message="leaderboard ranking count failed")
ERROR_71237 = ApiError(
    code="71237", message="leaderboard ranking not created for inactive leaderboard"
)
ERROR_71239 = ApiError(code="71239", message="leaderboard is not archived")
ERROR_71241 = ApiError(code="71241", message="forbidden environment")
ERROR_71242 = ApiError(code="71242", message="stat code not found in namespace")
ERROR_71243 = ApiError(code="71243", message="cycle doesn't belong to the stat code")
ERROR_71244 = ApiError(code="71244", message="cycle is already stopped")
