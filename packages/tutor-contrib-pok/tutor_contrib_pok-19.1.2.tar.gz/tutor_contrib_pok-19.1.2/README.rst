pok plugin for `Tutor <https://docs.tutor.edly.io>`__
#####################################################

Tutor plugin to integrate POK certificates into Open edX

About POK
*********

`POK <https://pok.tech>`_ revolutionizes credential management with powerful analytics and branding capabilities.

**Smart Credentials**

Track the real impact of your credentials with real-time metrics. See how many are viewed, shared on LinkedIn, or downloaded. Understand how they create career opportunities and improve your strategy based on concrete data.

**Brand Customization**

Customize every aspect of your credential experience - from pages to emails - with your logo, colors, and messages. Support for AI-powered automatic translations ensures a consistent brand experience globally.

**Actionable Insights**

Capture leads from your branded pages, access valuable insights on credential interactions, and download reports with one click. Our learning paths and analytics dashboards help improve user retention and drive growth.

Installation
************

.. code-block:: bash

    pip install git+https://github.com/aulasneo/tutor-contrib-pok

Usage
*****

.. code-block:: bash

    tutor plugins enable pok

After enabling the plugin, enable POK globally by creating and enabling the ``module_pok.enable`` waffle flag in the LMS:

- In the LMS Django Admin: Waffle -> Flags
- Create a flag named ``module_pok.enable`` and set it to "Active" (global ON)

By default, POK certificates are disabled until this flag is turned on. You can also set course or organization-specific overrides in the waffle flags configuration for more granular control.

Configuration
*************

The following settings can be configured in your Tutor environment:

- ``POK_API_KEY``: (Required) The API key for authenticating with the POK service. This key is used to validate requests between your Open edX instance and POK.
- ``POK_TEMPLATE_ID``: (Optional) The default template ID to use for certificates when no course-specific template is specified. If not set, you'll need to configure templates for each course individually.

Example configuration in ``config.yml``:

.. code-block:: yaml

    POK_API_KEY: "your-api-key-here"
    POK_TEMPLATE_ID: "default-template-id"  # Optional

Django Admin Configuration
**************************

After installation, two new sections will be available in the Django admin interface under "POK":

1. **Certificate Templates**

   - Map POK templates to specific courses
   - Fields:

     - **Course**: Select the course for this template
     - **Template ID**: The POK template ID to use
     - **Emission Type** (Optional):

       - 'POK' for standard PDF certificates (default)
       - 'Blockchain' for NFT certificates

     - **Page ID** (Optional): Custom page ID if defined in your POK site

2. **POK Certificates**

   - View and manage issued POK certificates

To access these settings:

1. Log in to the Django admin interface
2. Navigate to the "POK" section
3. Click on "Certificate templates" to manage course-specific templates
4. Click on "POK certificates" to view issued certificates

Version Management
******************

This project uses `bump2version <https://github.com/c4urself/bump2version>`_ to manage version numbers. The version is maintained in ``tutorpok/__about__.py``.

To install bump2version:

.. code-block:: bash

    pip install bump2version

To bump the version:

- For bug fixes (0.0.x): ``bump2version patch``
- For new features (0.x.0): ``bump2version minor``
- For breaking changes (x.0.0): ``bump2version major``