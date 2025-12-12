# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: operation-init.j2

"""Auto-generated package that contains models used by the AccelByte Gaming Services Iam Service."""

__author__ = "AccelByte"
__email__ = "dev@accelbyte.net"

# pylint: disable=line-too-long

from .authentication_with_pla_7019e1 import AuthenticationWithPlatformLinkV4
from .generate_token_by_new_h_19fd22 import GenerateTokenByNewHeadlessAccountV4
from .platform_token_grant_v4 import PlatformTokenGrantV4
from .platform_token_grant_v4 import (
    CodeChallengeMethodEnum as PlatformTokenGrantV4CodeChallengeMethodEnum,
)
from .request_target_token_re_d18562 import RequestTargetTokenResponseV4
from .simultaneous_login_v4 import SimultaneousLoginV4
from .simultaneous_login_v4 import (
    NativePlatformEnum as SimultaneousLoginV4NativePlatformEnum,
    CodeChallengeMethodEnum as SimultaneousLoginV4CodeChallengeMethodEnum,
)
from .token_grant_v4 import TokenGrantV4
from .token_grant_v4 import (
    GrantTypeEnum as TokenGrantV4GrantTypeEnum,
    CodeChallengeMethodEnum as TokenGrantV4CodeChallengeMethodEnum,
)
from .verify2fa_code_v4 import Verify2faCodeV4
