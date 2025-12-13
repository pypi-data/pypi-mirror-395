"""
TOS / policy building blocks for the lazy, in English language.

XXX DANGER! This is not replacement for legal advice. Contact your lawyer.

---

Copyright (c) 2025 Sakuragasaki46.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
See LICENSE for the specific language governing permissions and
limitations under the License.

This software is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

# TODO more snippets

from .strtools import SpitText


INDEMNIFY = """
You agree to indemnify and hold harmless {0} from any and all claims, damages, liabilities, costs and expenses, including reasonable and unreasonable counsel and attorney’s fees, arising out of any breach of this agreement.
"""

NO_WARRANTY = """
Except as represented in this agreement, the {0} is provided “AS IS”. Other than as provided in this agreement, {1} makes no other warranties, express or implied, and hereby disclaims all implied warranties, including any warranty of merchantability and warranty of fitness for a particular purpose.
"""

GOVERNING_LAW = """
These terms of services are governed by, and shall be interpreted in accordance with, the laws of {0}. You consent to the sole jurisdiction of {1} for all disputes between You and {2}, and You consent to the sole application of {3} law for all such disputes.
"""

ENGLISH_FIRST = """
In case there is any inconsistency between these Terms and any translation into other languages, the English language version takes precedence.
"""

EXPECT_UPDATES = """
{0} may periodically update these Terms of Service. Every time this happens, {0} will make its best efforts to notify You of such changes.

Whenever {0} updates these Terms of Service, Your continued use of the {0} platform constitutes Your agreement to the updated Terms of Service.
"""

SEVERABILITY = """
If one clause of these Terms of Service or any policy incorporated here by reference is determined by a court to be unenforceable, the remainder of the Terms and Content Policy shall remain in force.
"""

COMPLETENESS = """
These Terms, together with the other policies incorporated into them by reference, contain all the terms and conditions agreed upon by You and {0} regarding Your use of the {0} service. No other agreement, oral or otherwise, will be deemed to exist or to bind either of the parties to this Agreement.
"""


class Lawyer(SpitText):
    """
    A tool to ease the writing of Terms of Service for web apps.

    NOT A REPLACEMENT FOR A REAL LAWYER AND NOT LEGAL ADVICE

    *New in 0.11.0*
    """

    def __init__(self, /,
        app_name: str,      domain_name: str,
        company_name: str,  jurisdiction: str,
        country: str,       country_adjective: str
    ):
        self.app_name = app_name
        self.domain_name = domain_name
        self.company_name = company_name
        self.jurisdiction = jurisdiction
        self.country = country
        self.country_adjective = country_adjective

    def indemnify(self):
        return self.format(INDEMNIFY, 'app_name')

    def no_warranty(self):
        return self.format(NO_WARRANTY, 'app_name', 'company_name')

    def governing_law(self) -> str:
        return self.format(GOVERNING_LAW, 'country', 'jurisdiction', 'app_name', 'country_adjective')

    def english_first(self) -> str:
        return ENGLISH_FIRST
    
    def expect_updates(self) -> str:
        return self.format(EXPECT_UPDATES, 'app_name')

    def severability(self) -> str:
        return SEVERABILITY

    def completeness(self) -> str:
        return self.format(COMPLETENESS, 'app_name')

# This module is experimental and therefore not re-exported into __init__
__all__ = ('Lawyer',)