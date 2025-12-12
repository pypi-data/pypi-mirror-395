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

# AccelByte Gaming Services Iam Service

from accelbyte_py_sdk.core import ApiError

ERROR_422 = ApiError(code="422", message="request is unprocessable")
ERROR_10130 = ApiError(code="10130", message="user under age")
ERROR_10131 = ApiError(code="10131", message="invalid date of birth")
ERROR_10132 = ApiError(code="10132", message="invalid email address")
ERROR_10133 = ApiError(code="10133", message="email already used")
ERROR_10136 = ApiError(
    code="10136", message="code is either been used or not valid anymore"
)
ERROR_10137 = ApiError(code="10137", message="code is expired")
ERROR_10138 = ApiError(code="10138", message="code not match")
ERROR_10139 = ApiError(code="10139", message="platform account not found")
ERROR_10140 = ApiError(code="10140", message="user verified")
ERROR_10141 = ApiError(code="10141", message="email verified")
ERROR_10142 = ApiError(
    code="10142", message="new password cannot be same with original"
)
ERROR_10143 = ApiError(code="10143", message="password not match")
ERROR_10144 = ApiError(code="10144", message="user has no bans")
ERROR_10145 = ApiError(
    code="10145", message="disallow game access publisher user's ban"
)
ERROR_10146 = ApiError(code="10146", message="userID not match")
ERROR_10148 = ApiError(
    code="10148", message="verification code context doesn't match the required context"
)
ERROR_10149 = ApiError(code="10149", message="verification contact type doesn't match")
ERROR_10152 = ApiError(code="10152", message="verification code not found")
ERROR_10153 = ApiError(code="10153", message="user exist")
ERROR_10154 = ApiError(code="10154", message="country not found")
ERROR_10155 = ApiError(code="10155", message="country is not defined")
ERROR_10156 = ApiError(code="10156", message="role not found")
ERROR_10157 = ApiError(code="10157", message="specified role is not admin role")
ERROR_10158 = ApiError(code="10158", message="ban not found")
ERROR_10159 = ApiError(code="10159", message="operator is not a role manager")
ERROR_10160 = ApiError(code="10160", message="user already has the role")
ERROR_10161 = ApiError(code="10161", message="user already the role member")
ERROR_10162 = ApiError(code="10162", message="invalid verification")
ERROR_10163 = ApiError(
    code="10163", message="platform is already linked with the user account"
)
ERROR_10169 = ApiError(code="10169", message="age restriction not found")
ERROR_10170 = ApiError(code="10170", message="account is already a full account")
ERROR_10171 = ApiError(code="10171", message="email address not found")
ERROR_10172 = ApiError(
    code="10172", message="platform user is already linked with the account"
)
ERROR_10173 = ApiError(
    code="10173", message="platform is already linked with another user account"
)
ERROR_10174 = ApiError(code="10174", message="platform client not found")
ERROR_10175 = ApiError(code="10175", message="third party credential not found")
ERROR_10177 = ApiError(code="10177", message="username already used")
ERROR_10180 = ApiError(code="10180", message="admin invitation not found or expired")
ERROR_10182 = ApiError(
    code="10182", message="given namespace cannot be assigned to the role"
)
ERROR_10183 = ApiError(code="10183", message="unprocessable entity")
ERROR_10185 = ApiError(code="10185", message="publisher namespace not allowed")
ERROR_10188 = ApiError(code="10188", message="input validation field not found")
ERROR_10189 = ApiError(code="10189", message="invalid factor")
ERROR_10190 = ApiError(code="10190", message="auth secret key expired")
ERROR_10191 = ApiError(code="10191", message="email address not verified")
ERROR_10192 = ApiError(code="10192", message="factor not enabled")
ERROR_10193 = ApiError(code="10193", message="mfa not enabled")
ERROR_10194 = ApiError(code="10194", message="factor already enabled")
ERROR_10195 = ApiError(code="10195", message="no valid backup code found")
ERROR_10200 = ApiError(
    code="10200", message="link to a different platform account is not allowed"
)
ERROR_10202 = ApiError(code="10202", message="active device ban config already exists")
ERROR_10204 = ApiError(code="10204", message="device can not be banned")
ERROR_10207 = ApiError(code="10207", message="user namespace is not available")
ERROR_10208 = ApiError(code="10208", message="platform token expired")
ERROR_10213 = ApiError(code="10213", message="country is blocked")
ERROR_10215 = ApiError(code="10215", message="Simultaneous ticket is required")
ERROR_10216 = ApiError(code="10216", message="Native ticket is required")
ERROR_10217 = ApiError(
    code="10217",
    message="Native ticket's account linked AGS account has different linking history with input simultaneous ticket's",
)
ERROR_10218 = ApiError(
    code="10218",
    message="Simultaneous ticket's account linked AGS account has different linking history with input native ticket's",
)
ERROR_10219 = ApiError(
    code="10219",
    message="Native ticket's account linked AGS is already linked simultaneous but different with the input simultaneous ticket's",
)
ERROR_10220 = ApiError(
    code="10220",
    message="Native ticket's account linked AGS account is different with the one which simultaneous ticket's linked to",
)
ERROR_10221 = ApiError(
    code="10221",
    message="Simultaneous ticket's account linked AGS is already linked native but different with the input native ticket's",
)
ERROR_10222 = ApiError(code="10222", message="unique display name already exists")
ERROR_10226 = ApiError(code="10226", message="third party platform is not supported")
ERROR_10228 = ApiError(code="10228", message="invalid mfa token")
ERROR_10229 = ApiError(code="10229", message="request body exceed max limitation")
ERROR_10235 = ApiError(code="10235", message="date of birth not allowed to update")
ERROR_10236 = ApiError(code="10236", message="username not allowed to update")
ERROR_10237 = ApiError(code="10237", message="display name not allowed to update")
ERROR_10238 = ApiError(code="10238", message="country not allowed to update")
ERROR_10240 = ApiError(code="10240", message="namespace is not game namespace")
ERROR_10364 = ApiError(code="10364", message="client exists")
ERROR_10365 = ApiError(code="10365", message="client not found")
ERROR_10456 = ApiError(code="10456", message="role not found")
ERROR_10457 = ApiError(code="10457", message="specified role is not admin role")
ERROR_10459 = ApiError(code="10459", message="operator is not a role manager")
ERROR_10466 = ApiError(code="10466", message="invalid role members")
ERROR_10467 = ApiError(code="10467", message="role has no manager")
ERROR_10468 = ApiError(code="10468", message="role manager exist")
ERROR_10469 = ApiError(code="10469", message="role member exist")
ERROR_10470 = ApiError(code="10470", message="role is empty")
ERROR_20000 = ApiError(code="20000", message="internal server error")
ERROR_20001 = ApiError(code="20001", message="unauthorized access")
ERROR_20002 = ApiError(code="20002", message="validation error")
ERROR_20003 = ApiError(code="20003", message="forbidden access")
ERROR_20007 = ApiError(code="20007", message="too many requests")
ERROR_20008 = ApiError(code="20008", message="user not found")
ERROR_20009 = ApiError(code="20009", message="request_conflict")
ERROR_20013 = ApiError(code="20013", message="insufficient permissions")
ERROR_20019 = ApiError(code="20019", message="unable to parse request body")
ERROR_20021 = ApiError(code="20021", message="invalid pagination parameter")
ERROR_20022 = ApiError(code="20022", message="token is not user token")
ERROR_20024 = ApiError(code="20024", message="not implemented")
ERROR_20025 = ApiError(code="20025", message="not a publisher user")
ERROR_1014001 = ApiError(code="1014001", message="unable to parse request body")
ERROR_1014002 = ApiError(code="1014002", message="user already exists")
ERROR_1014016 = ApiError(code="1014016", message="unable to parse request body")
ERROR_1014017 = ApiError(code="1014017", message="user not found")
ERROR_1014018 = ApiError(code="1014018", message="verification code not found")
ERROR_1014019 = ApiError(code="1014019", message="verification code already used")
ERROR_1014020 = ApiError(code="1014020", message="verification code invalid")
ERROR_1014021 = ApiError(code="1014021", message="verification code expired")
ERROR_1015073 = ApiError(code="1015073", message="new password same as old password")
