# Copyright 2024-present Coinbase Global, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
#  limitations under the License.

import os
import json
from dataclasses import dataclass


@dataclass
class Credentials:
    access_key: str
    passphrase: str
    signing_key: str

    @staticmethod
    def from_json(data: str) -> 'Credentials':
        credentials_dict = json.loads(data)
        return Credentials(
            access_key=credentials_dict['accessKey'],
            passphrase=credentials_dict['passphrase'],
            signing_key=credentials_dict['signingKey']
        )

    @staticmethod
    def from_env(variable_name: str = 'INTX_CREDENTIALS') -> 'Credentials':
        # Lightweight .env loader (no external dependency). Loads only if not already in the environment.
        dotenv_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(dotenv_path):
            try:
                with open(dotenv_path, 'r') as f:
                    for raw_line in f:
                        line = raw_line.strip()
                        if not line or line.startswith('#') or '=' not in line:
                            continue
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        if value and len(value) >= 2:
                            if (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'"):
                                value = value[1:-1]
                        if key and key not in os.environ:
                            os.environ[key] = value
            except Exception:
                # Silently ignore .env parsing issues to avoid breaking users that set envs externally
                pass

        # Prefer single JSON env var if present
        env_var = os.getenv(variable_name)
        if env_var:
            return Credentials.from_json(env_var)

        # Fallback to three individual env vars
        access_key = os.getenv('INTX_ACCESS_KEY')
        passphrase = os.getenv('INTX_PASSPHRASE')
        signing_key = os.getenv('INTX_SIGNING_KEY')
        if access_key and passphrase and signing_key:
            return Credentials(access_key=access_key, passphrase=passphrase, signing_key=signing_key)

        raise EnvironmentError(
            f"Credentials not found. Set {variable_name} as JSON or INTX_ACCESS_KEY, INTX_PASSPHRASE, INTX_SIGNING_KEY (consider using a .env)."
        )
