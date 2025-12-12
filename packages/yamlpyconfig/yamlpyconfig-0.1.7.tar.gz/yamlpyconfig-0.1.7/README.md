# YAML Configuration Management: Local Files + Nacos Dynamic Configuration

This project provides a unified YAML configuration loading solution, supporting configuration retrieval from both **local files** and the **Nacos configuration center**. It also supports hot updates, variable substitution, decryption of encrypted values, and other advanced features.

Install the base dependency:

```bash
pip install yamlpyconfig
```

Enable Nacos support:

```bash
pip install yamlpyconfig[nacos]
```

------

## 1. Local YAML Configuration Loading

In the specified configuration directory (`config_dir`, e.g., `/config`), the following files must exist:

- `application.yaml` (**required**)
- `application-{profile}.yaml` (**optional**)

------

### 1.1 Profile Resolution and Loading Order

When initializing `ConfigManager`, the effective `profile` is determined using the following priority (highest → lowest):

1. `base_profile` explicitly passed to the `ConfigManager` constructor
2. Environment variable `APP_PROFILE`
3. Environment variable `SPRING_PROFILES_ACTIVE`
4. The `profile` field inside `application.yaml`
5. If none of the above is provided → **no** `application-{profile}.yaml` will be loaded

#### 1.1.1 Notes

- **`application.yaml` must exist**; otherwise an exception is raised.
- If a profile is determined but the corresponding `application-{profile}.yaml` is not found, an exception is thrown.

------

### 1.2 Extended Configuration: `extend-profiles`

Extended configurations come from **two sources**, and **both are loaded (merged)**:

1. The `extend-profiles` field inside `application.yaml` or `application-{profile}.yaml`
2. The `extend_profiles` parameter passed to the `ConfigManager` constructor

Both sources are comma-separated strings, where each entry represents one extension item.

Each extension item supports two forms.

------

#### 1.2.1 Two Extension Item Formats

| Type              | Example                       | Loading Behavior                                       |
| ----------------- | ----------------------------- | ------------------------------------------------------ |
| Explicit file     | `file:/full/path/to/xxx.yaml` | Loads the file at the given path; missing file → error |
| Extension profile | `dev-ext`                     | Loads `config_dir/application-dev-ext.yaml`            |

------

#### 1.2.2 Priority Rules

- Constructor-passed `extend_profiles` has higher priority than `extend-profiles` in YAML
- Within the same source, items appearing later have higher priority
- All extension configurations override values from `application.yaml` and `application-{profile}.yaml`

------

### 1.3 Overall Priority of Local Configurations (Low → High)

1. `application.yaml`
2. `application-{profile}.yaml`
3. `extend-profiles` (including both explicit file items and extension profile items)

------

## 2. Nacos Configuration Loading

To enable Nacos, define the `config-sources.nacos` section in `application.yaml`:

```yaml
config-sources:
  nacos:
    server-addr: "192.168.30.36:9090"
    namespace: "dev"
    group: "DEFAULT_GROUP"
    username: "nacos"
    password: "{encrypted}VuFvNZOg/q7ZQoIUGWydBw=="
    imports:
      - data-id: "gateway.yaml"
      - data-id: "application-ext.yaml"
```

------

### 2.1 Nacos Configuration Merge Order (Low → High)

1. Final merged result of all local configurations
2. Nacos `imports` in declared order (later items have higher priority)

------

## 3. Key Features and Usage Examples

------

### 3.1 Basic Usage

The following example demonstrates how configurations are loaded automatically and updated in real time:

```python
@pytest.mark.asyncio
async def test_config_manager_with_nacos(self):
    async with ConfigManager("./") as config_manager:
        logger.info(config_manager.get_config())
        while True:
            await asyncio.sleep(5)
            logger.info(config_manager.get_config())
    # Specify base_profile and extend_profiles
    async with ConfigManager("./", 
                             base_profile="dev", 
                             extend_profiles="file:./demo.yaml,dev-ext") as config_manager:
        logger.info(config_manager.get_config())
        while True:
            await asyncio.sleep(5)
            logger.info(config_manager.get_config())
```

Once inside the `async with` block:

- Local configuration is loaded
- If `config-sources.nacos` exists → connects to Nacos and enables hot updates

------

### 3.2 Environment Variable Placeholder Support

Local YAML files support Spring-style placeholders:

```yaml
key-with-default: ${KEY1:DEFAULT_VALUE}
key: ${KEY2}
```

Behavior:

- If the environment variable exists → use its value
- If not, and a default is provided → use the default
- If no default is provided → returns `None`

------

### 3.3 Encrypted Field Support (SM2 / SM4)

Sensitive fields (passwords, keys, etc.) can be declared with the `{encrypted}` prefix:

```yaml
password: "{encrypted}VuFvNZOg/q7ZQoIUGWydBw=="
```

To enable automatic decryption, specify the algorithm and key when initializing `ConfigManager`:

```python
@pytest.mark.asyncio
async def test_config_manager_with_nacos_decrypt(self):

    # Example using SM4 (symmetric key encryption)
    async with ConfigManager(
        "./",
        crypto_algorithm=AlgorithmEnum.SM4,
        key="lSU543Tes6wmjnb+PMVQNg=="
    ) as config_manager:

        logger.info(config_manager.get_config())
```

Notes:

- **SM4** → Symmetric encryption (a shared key is required)
- **SM2** → Asymmetric encryption (a private key must be provided)

