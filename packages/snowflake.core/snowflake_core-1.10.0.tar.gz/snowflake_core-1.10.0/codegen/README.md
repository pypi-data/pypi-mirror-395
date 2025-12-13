# OpenAPI code generation workflow

## Overview
This is a customized OpenAPI generator to generate Python REST client for SnowAPI.

### Custom Generator

There is a 'slightly'-modified version of the **[OpenAPI Generator 7.5.0](https://github.com/OpenAPITools/openapi-generator/tree/v7.5.0)** 
located under src/main/resources of this codegen/ directory.

One of the reasons for this slight tweak to the source code is to fix an underlying
bug in this version's handling of Handlebars templates with JDK versions >= 11,
described in this **[GitHub issue in handlebars.java](https://github.com/jknack/handlebars.java/issues/940)**.

That bug results in a: `java.lang.IllegalStateException: Shouldn't be illegal to access field 'size'` error
when running the codegen flow. The reason for that is that there is an illegal access to a property
in `java.util.HashMap` that is forbidden by the JVM. The fix is simply done by overriding
the `matches` method in `FieldValueResolver` of `handlebars.java` and adding an `&& isPublic` check
when trying to access illegal fields:

```java    
@Override
    public boolean matches(FieldWrapper field, String name) {
        return !isStatic(field) && field.getName().equals(name) && isPublic(field);
    }
```

The custom JAR simply packages this one-line fix into the OpenAPI generator's CLI, which we use
in `generate.py`.

## Usage

These instructions should be used when you want to update the PythonAPI REST
SDK bindings to the latest Snowflake REST API OpenAPI specs.

* Make sure you have access to this repo: `github.com/snowflake-eng/snowflake`
* Make sure you have `git`, `curl`, `mvn`, `java-11` installed

`./generate.py` is the script that generates the code from the [OpenAPI specs](https://github.com/snowflake-eng/snowflake/tree/main/GlobalServices/modules/snowapi/snowapi-codegen/src/main/openapi/specs)
in that repository.  It handles both cloning that repository locally, and
running the OpenAPI spec generator with our custom templates.

Try `./generate.py --help` for options and details.

You can generate the code against a commit other than `HEAD` on the spec repo
`main` branch by using the `--ref` option.

You can generate a subset of resources with the `-r`/`--resources` option, by
specifying a comma-separated list of resources, or by using `:all:` (the
default) to generate all supported resources.

## Generation history

As best we can, we try to capture details about the generation history so that
you can reproduce the generated code.  This history is kept in the
`spec_versions.json` file, which contains a mapping (stored in human readable
JSON format) from resource name to the commits and timestamp used to generate
that resource's code.

* Commit hash checked out from `dev-snowflake-rest-api-specs` used as the
  source YAML files.
* Closest commit from `main` of *this* repository that we could find.  This is
  tricky because you might be in a PR branch where the actually commit you're
  looking at will get squashed away.  The commit captured here may not be
  exactly right, but it's the best we can do and should help you reproduce the
  generation, if the mustache template files have changed since then.
* Timestamp the resource was generated, in ISO 8601 UTC format.
