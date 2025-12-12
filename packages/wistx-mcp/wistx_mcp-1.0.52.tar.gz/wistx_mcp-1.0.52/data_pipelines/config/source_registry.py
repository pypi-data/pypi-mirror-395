"""Source registry for automated discovery.

This file contains trusted domain patterns for automated source discovery.
Instead of manually curating individual URLs, we define domain patterns and
let the system automatically discover all relevant content.

Categories can be enabled/disabled using the 'enabled' flag at the category level.
Documentation categories are disabled by default - use on-demand research instead.
Compliance, pricing, and packages data remain enabled for scheduled pipelines.
"""

# Category enablement flags
# - compliance: ENABLED - Required for compliance standards processing
# - finops: DISABLED - Use on-demand research for freshness
# - architecture: DISABLED - Use on-demand research for freshness
# - security: DISABLED - Use on-demand research for freshness
# - devops: DISABLED - Use on-demand research for freshness
# - platform: DISABLED - Use on-demand research for freshness
# - sre: DISABLED - Use on-demand research for freshness
CATEGORY_ENABLED = {
    "compliance": True,   # Keep enabled - compliance standards don't change frequently
    "finops": False,      # Disabled - documentation can become stale
    "architecture": False,  # Disabled - documentation can become stale
    "security": False,    # Disabled - documentation can become stale
    "devops": False,      # Disabled - documentation can become stale
    "platform": False,    # Disabled - documentation can become stale
    "sre": False,         # Disabled - documentation can become stale
}


def is_category_enabled(category: str) -> bool:
    """Check if a category is enabled for pre-crawling.

    Args:
        category: The category name (compliance, finops, etc.)

    Returns:
        True if the category is enabled, False otherwise
    """
    return CATEGORY_ENABLED.get(category, False)


def get_enabled_categories() -> list[str]:
    """Get list of enabled categories.

    Returns:
        List of enabled category names
    """
    return [cat for cat, enabled in CATEGORY_ENABLED.items() if enabled]


def get_disabled_categories() -> list[str]:
    """Get list of disabled categories.

    Returns:
        List of disabled category names
    """
    return [cat for cat, enabled in CATEGORY_ENABLED.items() if not enabled]


TRUSTED_DOMAINS = {
    "compliance": {
        "tier_1": [
            {
                "domain": "pcisecuritystandards.org",
                "discovery_mode": "sitemap",
                "path_patterns": ["/document_library/", "/requirements/"],
                "content_types": ["pdf", "html"],
            },
            {
                "domain": "hhs.gov",
                "discovery_mode": "sitemap",
                "path_patterns": ["/hipaa/"],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "csrc.nist.gov",
                "discovery_mode": "sitemap",
                "path_patterns": ["/publications/"],
                "content_types": ["pdf", "xml", "json"],
            },
            {
                "domain": "iso.org",
                "discovery_mode": "sitemap",
                "path_patterns": ["/standard/"],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "gdpr.eu",
                "discovery_mode": "sitemap",
                "path_patterns": ["/"],
                "content_types": ["html"],
            },
            {
                "domain": "fedramp.gov",
                "discovery_mode": "sitemap",
                "path_patterns": ["/documents/", "/assets/"],
                "content_types": ["pdf", "html"],
            },
        ],
        "tier_2": [
            {
                "domain": "github.com",
                "discovery_mode": "search",
                "search_queries": [
                    "PCI-DSS compliance",
                    "HIPAA requirements",
                    "SOC2 controls",
                ],
                "content_types": ["markdown", "yaml"],
            },
        ],
    },
    "finops": {
        "tier_1": [
            {
                "domain": "aws.amazon.com",
                "discovery_mode": "sitemap",
                "path_patterns": [
                    "/well-architected/",
                    "/pricing/",
                    "/cost-management/",
                    "/whitepapers/",
                ],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "cloud.google.com",
                "discovery_mode": "sitemap",
                "path_patterns": [
                    "/cost-management/",
                    "/pricing/",
                    "/architecture/",
                ],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "azure.microsoft.com",
                "discovery_mode": "sitemap",
                "path_patterns": [
                    "/cost-management/",
                    "/pricing/",
                    "/architecture/",
                ],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "finops.org",
                "discovery_mode": "sitemap",
                "path_patterns": ["/resources/", "/guides/"],
                "content_types": ["html", "pdf"],
            },
        ],
    },
    "architecture": {
        "tier_1": [
            {
                "domain": "aws.amazon.com",
                "discovery_mode": "sitemap",
                "path_patterns": [
                    "/architecture/",
                    "/solutions/",
                    "/reference-architectures/",
                    "/whitepapers/",
                ],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "cloud.google.com",
                "discovery_mode": "sitemap",
                "path_patterns": [
                    "/architecture/",
                    "/solutions/",
                    "/reference-architectures/",
                ],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "azure.microsoft.com",
                "discovery_mode": "sitemap",
                "path_patterns": [
                    "/architecture/",
                    "/solutions/",
                    "/reference-architectures/",
                ],
                "content_types": ["html", "pdf"],
            },
        ],
    },
    "security": {
        "tier_1": [
            {
                "domain": "owasp.org",
                "discovery_mode": "sitemap",
                "path_patterns": ["/www-project-", "/cheat/"],
                "content_types": ["html", "markdown"],
            },
        ],
        "tier_2": [
            {
                "domain": "github.com",
                "discovery_mode": "search",
                "search_queries": ["OWASP Top 10"],
                "content_types": ["markdown", "yaml"],
            },
        ],
        "tier_3": [
            {
                "domain": "github.com",
                "discovery_mode": "search",
                "search_queries": ["OWASP Top 10"],
                "content_types": ["markdown", "yaml"],
            },
        ],
    },
    "devops": {
        "tier_1": [
            {
                "domain": "kubernetes.io",
                "discovery_mode": "sitemap",
                "path_patterns": ["/docs/", "/blog/"],
                "content_types": ["html", "markdown"],
            },
            {
                "domain": "terraform.io",
                "discovery_mode": "sitemap",
                "path_patterns": ["/docs/", "/registry/"],
                "content_types": ["html", "markdown"],
            },
            {
                "domain": "cncf.io",
                "discovery_mode": "sitemap",
                "path_patterns": ["/blog/", "/resources/"],
                "content_types": ["html"],
            },
        ],
    },
    "platform": {
        "tier_1": [
            {
                "domain": "backstage.io",
                "discovery_mode": "sitemap",
                "path_patterns": ["/docs/", "/blog/"],
                "content_types": ["html", "markdown"],
            },
            {
                "domain": "cncf.io",
                "discovery_mode": "sitemap",
                "path_patterns": ["/blog/", "/resources/"],
                "content_types": ["html"],
            },
            {
                "domain": "platformengineering.org",
                "discovery_mode": "sitemap",
                "path_patterns": ["/"],
                "content_types": ["html"],
            },
        ],
    },
    "sre": {
        "tier_1": [
            {
                "domain": "sre.google",
                "discovery_mode": "sitemap",
                "path_patterns": ["/books/", "/workbook/"],
                "content_types": ["html", "pdf"],
            },
            {
                "domain": "landing.google.com",
                "discovery_mode": "sitemap",
                "path_patterns": ["/sre/"],
                "content_types": ["html"],
            },
            {
                "domain": "cncf.io",
                "discovery_mode": "sitemap",
                "path_patterns": ["/blog/", "/resources/"],
                "content_types": ["html"],
            },
        ],
    },
}

MANUAL_URLS = {
    "compliance": {
        "PCI-DSS": [
            "https://www.pcisecuritystandards.org/document_library/",
            "https://help.drata.com/en/articles/6038558-required-documentation-for-pci-dss",
            "https://sprinto.com/blog/pci-dss-controls/",
            "https://www.crowdstrike.com/en-us/cybersecurity-101/data-protection/pci-dss-requirements/",
            "https://drata.com/blog/pci-compliance-checklist",
            "https://blog.rsisecurity.com/how-many-pci-controls-are-there/",
            "https://documentation.suse.com/compliance/all/pdf/article-security-pcidss_en.pdf",
            "https://listings.pcisecuritystandards.org/documents/pci_ssc_quick_guide.pdf",
            "https://www.middlebury.edu/sites/default/files/2025-01/PCI-DSS-v4_0_1.pdf?fv=AKHVQBp6",
            "https://www.crowdstrike.com/en-us/cybersecurity-101/data-protection/pci-dss-requirements/",
            "https://stripe.com/guides/pci-compliance",
            "https://www.isdecisions.com/en/blog/compliance/pci-dss-access-compliance",
            "https://auditboard.com/blog/pci-dss-requirements",
            "https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-pci-dss-v4-including-global-resource-types.html"
        ],
        "CIS-AWS": [
           "https://www.cisecurity.org/benchmark/aws",
                "https://www.cisecurity.org/benchmark/amazon_web_services",
                "https://www.xavor.com/blog/how-to-implement-cis-benchmarks-on-aws-using-aws-config-and-security-hub/",
                "https://docs.aws.amazon.com/securityhub/latest/userguide/cis-aws-foundations-benchmark.html",
                "https://docs.aws.amazon.com/audit-manager/latest/userguide/CIS-controls.html",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Amazon_Linux_2_Benchmark_v1.0.0.pdf",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Amazon_Linux_Benchmark_v2.1.0.pdf",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Amazon_Web_Services_Foundations_Benchmark_v1.2.0.pdf",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Amazon_Web_Services_Three-tier_Web_Architecture_Benchmark_v1.0.0.pdf"
        ],
        "CIS-GCP": [
           "https://www.cisecurity.org/benchmark/google_cloud_platform",
                "https://www.cisecurity.org/benchmark/gcp",
                "https://databrackets.com/services/google-cloud-platform-gcp-security-assessment/",
                "https://www.clouddefense.ai/cis-benchmarks-for-google-cloud-platform/",
                "https://github.com/GoogleCloudPlatform/inspec-gcp-cis-benchmark",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Google_Cloud_Platform_Foundation_Benchmark_v1.0.0.pdf"
        ],
        "CIS-Azure": [
           "https://www.cisecurity.org/benchmark/azure",
                "https://www.cisecurity.org/benchmark/microsoft_azure",
                "https://learn.microsoft.com/en-us/security/benchmark/azure/overview-v3",
                "https://learn.microsoft.com/en-us/security/benchmark/azure/overview-v2",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Microsoft_Azure_Foundations_Benchmark_v1.1.0.pdf"
        ],
        "HIPAA": [
            "https://www.hhs.gov/hipaa/for-professionals/security/",
            "https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/",
            "https://www.hhs.gov/hipaa/for-professionals/security/guidance/",
            "https://www.hhs.gov/sites/default/files/ocr/privacy/hipaa/administrative/securityrule/techsafeguards.pdf",
            "https://www.accountablehq.com/post/breaking-down-technical-safeguards",
            "https://www.hipaajournal.com/hipaa-privacy-rule/",
            "https://www.kiteworks.com/hipaa-compliance/hipaa-compliance-requirements/",
            "https://blog.hushmail.com/blog/hipaa-technical-safeguards",
            "https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodm/602518m.pdf",
            "https://rublon.com/blog/hipaa-compliance-access-control-authentication/",
            "https://www.law.cornell.edu/cfr/text/45/164.312",
            "https://privacyruleandresearch.nih.gov/pdf/hipaa_booklet_4-14-2003.pdf",
            "https://www.securitymetrics.com/blog/how-meet-hipaa-documentation-requirements",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/HIPAA-omnibus-rule.html"
        ],
        "SOC2": [
            "https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html",
            "https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome.html",
            "https://secureframe.com/hub/soc-2/compliance-documentation",
            "https://cynomi.com/soc2/soc-2-audit-checklist/",
            "https://sprinto.com/blog/soc-2-trust-principles/",
            "https://www.vanta.com/collection/soc-2/soc-2-compliance-requirements",
            "https://kirkpatrickprice.com/wp-content/uploads/2017/02/SOC-2-Compliance-Handbook_Whitepaper.pdf",
            "https://www.cbh.com/insights/articles/soc-2-trust-services-criteria-guide/",
            "https://auditboard.com/blog/soc-2-framework-guide-the-complete-introduction",
            "http://www.sfisaca.org/images/FC15_Presentations/C33.pdf",
            "https://secureframe.com/hub/soc-2/trust-services-criteria",
            "https://scytale.ai/resources/steps-to-ready-your-soc-2-compliance-documentation/"
        ],
        "NIST-800-53": [
            "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
            "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf",
            "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final/xml",
            "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final/json",
            "https://auditboard.com/blog/fundamentals-of-nist-cybersecurity-framework-controls",
            "https://sprinto.com/blog/nist-800-53-guide/",
            "https://www.rapid7.com/globalassets/_pdfs/whitepaperguide/rapid7-nist-800-171-compliance-guide.pdf",
            "https://hyperproof.io/resource/a-complete-guide-to-nist-compliance/",
            "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r3.pdf",
            "https://www.zengrc.com/resources/guide/guide-complete-guide-to-the-nist-cybersecurity-framework/",
            "https://www.cybersaint.io/blog/nist-800-53-control-families",
            "https://www.uc.edu/content/dam/uc/infosec/docs/Guidelines/NIST_171_Compliance_Guideline.pdf",
            "https://www.coro.net/glossary/nist-cybersecurity-framework",
            "https://www.portnox.com/cybersecurity-101/nist-sp-800-53-access-control-requirements/",
            "https://services.google.com/fh/files/misc/gcp_nist_cybersecurity_framework.pdf",
            "https://aws.amazon.com/blogs/security/implementing-a-compliance-and-reporting-strategy-for-nist-sp-800-53-rev-5/",
            "https://docs.aws.amazon.com/securityhub/latest/userguide/standards-reference-nist-800-53.html",
            "https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_5.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/NIST800-53r5.html"
        ],
        "ISO-27001": [
            "https://www.iso.org/standard/27001",
            "https://cdn.standards.iteh.ai/samples/82875/726bcf58250e43d9a666b4d929c8fbdb/ISO-IEC-27001-2022.pdf",
            "https://amnafzar.net/files/1/ISO%2027000/ISO%20IEC%2027001-2013.pdf",
            "https://en.wikipedia.org/wiki/ISO/IEC_27001",
            "https://secureframe.com/hub/iso-27001/audit-documentation",
            "https://www.isms.online/iso-27001/",
            "https://sprinto.com/blog/iso-27001-mandatory-documents/",
            "https://pecb.com/en/education-and-certification-for-individuals/iso-iec-27001",
            "https://assets.ctfassets.net/ueprkma36dz5/757aZjJOZ0F6rhdVmKPdaw/e66cd584dcb9a64b632d50f4671dcaf4/A-Comprehensive-Guide-to-the-ISO-27001.pdf",
            "https://www.isms.online/iso-27001/iso-27001-guide-for-beginners/",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/iso-27001-2013.html"
        ],
        "GDPR": [
            "https://gdpr-info.eu/",
            "https://gdpr.eu/what-is-gdpr/",
            "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679",
            "https://euro.ecom.cmu.edu/program/law/08-732/Privacy/GDPRPocketGuide.pdf",
            "https://advisera.com/articles/list-of-mandatory-documents-required-by-eu-gdpr/",
            "https://advisera.com/gdpr/",
            "https://www.thoropass.com/blog/gdpr-compliance-checklist",
            "https://www.itgovernance.eu/blog/en/summary-of-the-gdprs-10-key-requirements",
            "https://www.processunity.com/resources/blogs/6-security-controls-need-general-data-protection-regulation-gdpr/",
            "https://www.tableau.com/learn/articles/gdpr-resources",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/GDPR.html"
        ],
        "FedRAMP": [
            "https://www.fedramp.gov/documents/",
            "https://www.fedramp.gov/assets/resources/documents/FedRAMP_Security_Controls_Baseline.xlsx",
            "https://www.fedramp.gov/assets/resources/documents/FedRAMP_Security_Controls_Baseline.pdf",
            "https://www.fedramp.gov/resources/documents/rev4/REV_4_CSP_Authorization_Playbook_Getting_Started_with_FedRAMP.pdf",
            "https://www.fedramp.gov/resources/documents/Agency_Authorization_Playbook.pdf",
            "https://www.fedramp.gov/resources/training/200-A-FedRAMP-Training-FedRAMP-System-Security-Plan-SSP-Required-Documents.pdf",
            "https://linfordco.com/blog/fedramp-compliance/",
            "https://www.zengrc.com/blog/conducting-a-fedramp-risk-assessment/",
            "https://www.aquasec.com/cloud-native-academy/cloud-compliance/fedramp-compliance/",
            "https://www.zengrc.com/blog/conducting-a-fedramp-risk-assessment/",
            "https://www.energy.gov/sites/default/files/2025-02/DOE%20FedRAMP%20Agency%20Authorization%20Process%20Guide_v1.2_Signed.pdf",
            "https://auditboard.com/blog/fedramp-checklist",
            "https://security.cms.gov/learn/fedramp"
        ],
        "CCPA": [
            "https://oag.ca.gov/privacy/ccpa",
            "https://oag.ca.gov/privacy/ccpa/regulations",
            "https://trustarc.com/resource/ccpa-guide/",
            "https://www.securitycompass.com/blog/ccpa-compliance-checklist-a-step-by-step-guide-for-businesses/",
            "https://captaincompliance.com/education/new-ccpa-2026-regulations-your-complete-compliance-action-guide/",
            "https://en.wikipedia.org/wiki/California_Consumer_Privacy_Act",
            "https://www.cookieyes.com/blog/how-to-comply-with-ccpa/",
            "https://www.metricstream.com/learn/ccpa-compliance-guide.html",
            "https://www.huschblackwell.com/ccpa",
            "https://aws.amazon.com/blogs/security/tag/ccpa/",
            "https://hyperproof.io/resource/what-is-ccpa-compliance-a-beginners-guide/",
            "https://www.networkintelligence.ai/blogs/ccpa-compliance-checklist-your-2025-guide/",
            "https://auth0.com/ccpa",
            "https://oag.ca.gov/privacy/ccpa",
            "https://cloud.google.com/blog/products/identity-security/supporting-our-customers-with-the-california-consumer-privacy-act",
            "https://services.google.com/fh/files/misc/googlecloud_ccpa_ccra_whitepaper.pdf"
        ],
        "SOX": [
             "https://www.sec.gov/corpfin/sec-guide-sarbanes-oxley-act-2002",
            "https://www.sec.gov/rules/final/33-8238.htm",
            "https://www.ibm.com/think/topics/sox-compliance",
            "https://www.cbh.com/insights/articles/what-are-sox-controls-common-types-and-implementation-tips/",
            "https://www.safepaas.com/resources/Guidebook-SOX-Internal-Controls-Compliance.pdf",
            "https://veza.com/blog/sox-compliance-checklist/",
            "https://www.metricstream.com/insights/sox-it-controls.htm"
            "https://www.auditanalytics.com/doc/SOX_404_Disclosures_An_Eighteen-Year_Review.pdf",
            "https://auditboard.com/blog/sox-compliance"
            "https://www.itgovernanceusa.com/sarbanes-oxley",
            "https://www.sec.gov/files/rules/proposed/s74002/card941503.pdf",
            "https://www.fortinet.com/resources/cyberglossary/sox-sarbanes-oxley-act"
        ],
        "GLBA": [
            "https://www.ftc.gov/business-guidance/privacy-security/gramm-leach-bliley-act",
            "https://www.ftc.gov/tips-advice/business-center/privacy-and-security/gramm-leach-bliley-act",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/gramm-leach-bliley-act.html",
            "https://policies.vpfa.fsu.edu/policies-and-procedures/technology/gramm-leach-bliley-act-glb-policy",
            "https://www.formassembly.com/blog/glba-compliance-pocket-guide/",
            "https://uscode.house.gov/view.xhtml?req=granuleid%3AUSC-prelim-title15-chapter94&saved=%7CZ3JhbnVsZWlkOlVTQy1wcmVsaW0tdGl0bGUxNS1zZWN0aW9uNjgwMQ%3D%3D%7C%7C%7C0%7Cfalse%7Cprelim&edition=prelim",
            "https://www.purdue.edu/securepurdue/security-programs/GLBA-HIPAA-security-program/full-document.php",
            "https://www.digitalguardian.com/blog/what-glba-compliance-understanding-data-protection-requirements-gramm-leach-bliley-act",
            "https://www.innreg.com/blog/glba-compliance-privacy-and-safeguards-rule",
            "https://www.wisconsin.edu/uw-policies/download/Guide-to-GLBA-Safeguards-Rule-v1.1.pdf",
            "https://it.fdu.edu/gramm-leach-bliley-policy/",
            "https://www.thompsoncoburn.com/wp-content/uploads/2024/11/Click-here.pdf",
            "https://www.fdic.gov/regulations/compliance/manual/8/viii-1.1.pdf"
        ],
        "GENERAL_DATA_PROTECTION_REGULATION": [
            "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Docker_1.13.0_Benchmark_v1.0.0.pdf",
            "https://github.com/jonathanbglass/cis-benchmarks",
            "https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-Security-Identity-and-Compliance-Services.html",
            "https://docs.aws.amazon.com/config/latest/developerguide/conformancepack-sample-templates.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/framework-overviews.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/GDPR.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/SOX.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/GLBA.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/CCPA.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/HIPAA.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/SOC2.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/NIST-800-53.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/ISO-27001.html",
            "https://docs.aws.amazon.com/audit-manager/latest/userguide/FedRAMP.html",
            "https://www.wiz.io/academy/nist-compliance",
            "https://www.wiz.io/academy/cloud-compliance-fast-track-guide",
            "https://www.wiz.io/academy/federal-information-security-management-act-fisma",
            "https://www.wiz.io/academy/hipaa-cloud-compliance",
            "https://www.wiz.io/academy/cybersecurity-maturity-model-certification-cmmc",
            "https://www.wiz.io/academy/cloud-governance",
            "https://www.wiz.io/academy/cis-benchmarks",
            "https://www.wiz.io/academy/iso-27001-controls",
            "https://www.wiz.io/academy/cloud-governance",
            "https://www.wiz.io/academy/operationalizing-cloud-governance",
            "https://www.wiz.io/academy/cloud-governance-best-practices",
            "https://www.wiz.io/academy/cloud-compliance-fast-track-guide"
        ],
    },
    "finops": {
        "GCP_COST_MANAGEMENT": [
            "https://docs.cloud.google.com/docs/costs-usage",
            "https://cloud.google.com/cost-management/pricing",
            "https://cloud.google.com/cost-management/budget",
            "https://cloud.google.com/cost-management/budget/create-budget",
            "https://cloud.google.com/cost-management/budget/create-budget",
        ],
        "AWS_COST_MANAGEMENT": [
            "https://docs.aws.amazon.com/account-billing/",


            "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html",

            "https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html",

            "https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html",
        ],
        "AZURE_COST_MANAGEMENT": [
           "https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/",

            "https://learn.microsoft.com/en-us/azure/cost-management-billing/",

        ],
        "FINOPS_BEST_PRACTICES_OPTIMIZATION_OPPORTUNITIES": [
            "https://www.wiz.io/academy/cloud-cost-optimization",
            "https://www.wiz.io/academy/azure-cost-optimization",
            "https://www.wiz.io/academy/aws-cost-optimization",
            "https://www.wiz.io/academy/s3-cost-optimization",
            "https://www.wiz.io/academy/ecs-cost-optimization",
            "https://www.wiz.io/academy/kubernetes-cost-optimization",
            "https://www.wiz.io/academy/azure-vs-aws-cloud-cost",
            "https://www.wiz.io/academy/aws-cost",
            "https://spot.io/resources/cloud-cost/cloud-cost-optimization-15-ways-to-optimize-your-cloud/",

            "https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html",
            "https://www.cloudbolt.io/cloud-cost-management/cloud-cost-optimization/",
            "https://lucid.co/blog/cloud-cost-optimization-guide",
            "https://www.prosperops.com/blog/cloud-cost-optimization/",
            "https://www.flexera.com/products/flexera-one/cloud-cost-optimization",
            "https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/",
            "https://edgedelta.com/company/blog/azure-cost-optimization",
            "https://www.rishabhsoft.com/blog/azure-cost-optimization",
            "https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/principles",
            "https://nearshore-it.eu/articles/azure-cloud-costs-optimization/",
            "https://www.lucidity.cloud/blog/azure-cost-optimization-checklist",
            "https://cloud.google.com/blog/topics/cost-management/best-practices-for-optimizing-your-cloud-costs",
            "https://docs.cloud.google.com/architecture/framework/cost-optimization",
            "https://docs.cloud.google.com/architecture/framework/cost-optimization",
            "https://cast.ai/blog/gcp-cost-optimization/",
            "https://www.lucidity.cloud/blog/gcp-cost-optimization-best-practices",
            "https://66degrees.com/your-google-cloud-cost-optimization-checklist/",
            "https://medium.com/google-cloud/gcp-checklist-8-cost-optimisation-381370d3748",
            "https://ternary.app/blog/gcp-cost-optimization-guide/",
            "https://www.cloudkeeper.com/insights/blog/gcp-cost-optimization-top-10-effective-strategies-maximum-impact",
            "https://followrabbit.ai/blog/the-ultimate-guide-for-gcp-cost-optimization-part-1",
            "https://www.dnsstuff.com/cloud-cost-optimization",
            "https://www.finout.io/blog/understanding-and-optimizing-google-cloud-storage-costs-a-finops-perspective",
            "https://www.dnsstuff.com/cloud-cost-optimization",

            "https://www.cloudlaya.com/blog/guide-to-cloud-cost-optimization/",
            "https://bluelight.co/blog/google-cloud-cost-optimization",
            "https://www.netapp.com/blog/3-ways-to-save-big-and-10-price-variations-to-know-aws-cvo-blg/",
            "https://stratusgrid.com/blog/aws-cost-optimization-guide",
            "https://medium.com/@mohammedalaa/aws-cost-optimization-your-monthly-to-do-list-b73f471d41ca",
            "https://cloudgov.ai/resources/blog/master-aws-cloud-cost-optimization/",
            "https://aws.amazon.com/blogs/containers/cost-optimization-checklist-for-ecs-fargate/",
            "https://www.lucidity.cloud/blog/aws-cost-optimization-checklist",
            "https://medium.com/@kaushal_24935/the-ultimate-aws-cost-optimization-checklist-for-2025-192dc11615e2",
            "https://www.naviteq.io/blog/aws-cost-optimization-best-practices-proven-strategies-to-cut-cloud-expenses/",
            "https://dev.to/aws-builders/mastering-aws-cost-optimization-practical-tips-to-save-big-3cao",
            "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html",
            "https://www.stormit.cloud/blog/aws-cost-optimization/",
            "https://www.freecodecamp.org/news/cost-optimization-in-aws/",
            "https://aws.amazon.com/blogs/containers/cost-optimization-checklist-for-ecs-fargate/",
            "https://aws.amazon.com/blogs/aws/new-savings-plans-for-aws-compute-services/",

            "https://aws.amazon.com/blogs/containers/optimize-cost-for-container-workloads-with-ecs-capacity-providers-and-ec2-spot-instances/",
            "https://ec2spotworkshops.com/ecs-spot-capacity-providers.html",

            "https://zesty.co/blog/5-cloud-cost-optimization-savings/",
            "https://www.cloudkeeper.com/insights/blog/gcp-cost-optimization-top-10-effective-strategies-maximum-impact",
            "https://followrabbit.ai/blog/the-ultimate-guide-for-gcp-cost-optimization-part-1",
            "https://www.dnsstuff.com/cloud-cost-optimization",
            "https://www.finout.io/blog/understanding-and-optimizing-google-cloud-storage-costs-a-finops-perspective",
            "https://www.dnsstuff.com/cloud-cost-optimization",
            "https://www.cloudlaya.com/blog/guide-to-cloud-cost-optimization/",
            "https://bluelight.co/blog/google-cloud-cost-optimization",
            "https://www.netapp.com/blog/3-ways-to-save-big-and-10-price-variations-to-know-aws-cvo-blg/",
            "https://stratusgrid.com/blog/aws-cost-optimization-guide",
            "https://docs.public.content.oci.oraclecloud.com/en-us/iaas/Content/Billing/Tasks/signingup_topic-Estimating_Costs.htm",
            "https://next.api.alibabacloud.com/",
            "https://www.finops.org/wg/finops-for-data-center-structuring-data-center-cost-and-usage-data/#:~:text=A%20FinOps%20Scope%20refers%20to,spending%20beyond%20public%20cloud%20services",
            "https://www.finops.org/wg/cloud-cost-allocation/#:~:text=FinOps%20practitioners%20most%20often%20apply,like%20offerings%20provided%20by%20CSPs",
            "https://www.finops.org/wg/adopting-focus-the-finops-open-cost-and-usage-specification/#:~:text=FinOps%20Open%20Cost%20and%20Usage%20Specification%20(FOCUS%E2%84%A2)%20is%20an,%E2%84%A2%20see%20the%20below%20resources",
            "https://www.finops.org/wg/how-to-build-and-optimize-finops-data-workflows/#:~:text=In%20early%20stages%20of%20a,all%20of%20your%20data%20sources",
        ],


    },
    "architecture": {
        "infrastructure_and_devops_design_principles": [
            "https://www.google.com/aclk?sa=L&ai=DChsSEwjthIuTue2QAxXuhlAGHV1tNpQYACICCAEQAxoCZGc&co=1&gclid=CjwKCAiA_dDIBhB6EiwAvzc1cNHqhTXtBhSDWUPQddFjLyO9rBbe7uPvT3zlkMA_Jk0PlUlunupxPBoCidEQAvD_BwE&cce=2&sig=AOD64_3w48NwUWvT1pf-FrOYeHIzvZqrMw&q&adurl&ved=2ahUKEwjDhIOTue2QAxXzQUEAHdU7FPMQ0Qx6BAgPEAE",

            "https://learn.microsoft.com/en-us/azure/architecture/guide/devops/devops-start-here",

            "https://lukeshaughnessy.medium.com/10-principles-for-successful-devops-infrastructure-architecture-6b98b521eeb",

            "https://www.atlassian.com/devops/what-is-devops",

            "https://aws.amazon.com/blogs/architecture/lets-architect-devops-best-practices-on-aws/",

            "https://testrigor.com/blog/devops-a-software-architects-perspective/",

            "https://www.prismetric.com/devops-architecture/",

            "https://cloud.google.com/blog/products/application-development/5-principles-for-cloud-native-architecture-what-it-is-and-how-to-master-it",

            "https://docs.aws.amazon.com/wellarchitected/latest/framework/oe-design-principles.html",

            "https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/",

            "https://medium.com/@bijit211987/cloud-architecture-considerations-framework-427a08e5c646",

            "https://miro.com/diagramming/aws-cloud-architecture-design-principles/",
            "https://docs.cloud.google.com/architecture",

            "https://medium.com/@laddadamey/google-cloud-architecture-framework-system-design-f1f569f1b541",

            "https://docs.cloud.google.com/architecture/framework",

            "https://niveussolutions.com/google-cloud-architecture-foundations-and-benefits/",

            "https://mycloudwiki.com/cloud/design-principles-to-build-robust-cloud-solutions/",

            "https://saraswathilakshman.medium.com/9-principles-of-cloud-architecture-a-practical-guide-254006f83d7a",  
        ],
        "CLOUD_DOCS": [
            "https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/architecture.html",
            "https://docs.aws.amazon.com/",
            "https://docs.aws.amazon.com/sitemap_index.xml",
            "https://docs.cloud.google.com/docs",
            "https://cloud.google.com/docs/",
            "https://cloud.google.com/sitemap.xml",
            "https://cloud.google.com/sitemap_index.xml",
            "https://learn.microsoft.com/en-us/azure/architecture/",
            "https://learn.microsoft.com/en-us/azure/architecture/sitemap.xml",
            "https://learn.microsoft.com/en-us/azure/architecture/sitemap_index.xml",
            "https://learn.microsoft.com/en-us/azure/architecture/docs/",
            "https://learn.microsoft.com/en-us/azure/architecture/docs/sitemap.xml",
            "https://learn.microsoft.com/en-us/azure/architecture/docs/sitemap_index.xml",
            "https://learn.microsoft.com/_sitemaps/sitemapindex.xml",

            "https://learn.microsoft.com/answers/sitemaps/sitemap.xml",
            "https://learn.microsoft.com/answers/sitemaps/sitemap_index.xml",
            "https://learn.microsoft.com/answers/sitemaps/sitemap.xml",
            "https://docs.oracle.com/en/database/index.html",

            "https://docs.oracle.com/en/database/oracle/oracle-database/index.html",
            "https://www.alibabacloud.com/help/en/",
            "https://www.ibm.com/docs/en",
            "https://devcenter.heroku.com/categories/reference",
            "https://docs.vultr.com/",
            "https://vercel.com/docs",
            "https://docs.railway.com/",
            "https://docs.digitalocean.com/",
            "https://www.linode.com/docs/",
        ]

    },
    "security": {
        "cloud_security": [
            "https://www.wiz.io/academy/what-is-cloud-security",
            "https://www.wiz.io/academy/cloud-security-strategy",
            "https://www.wiz.io/academy/cloud-security-architecture",
            "https://www.wiz.io/academy/what-is-a-cloud-native-application-protection-platform-cnapp",
            "https://www.wiz.io/academy/what-is-cloud-security-posture-management-cspm",
            "https://www.wiz.io/academy/what-is-vulnerability-management",
            "https://www.wiz.io/academy/vulnerability-scanning",
            "https://www.wiz.io/academy/vulnerability-management-best-practices",
            "https://www.wiz.io/academy/vulnerability-prioritization",
            "https://www.wiz.io/academy/risk-based-vulnerability-management",
            "https://www.wiz.io/academy/oss-vulnerability-management-tools",
            "https://www.wiz.io/academy/cloud-infrastructure-entitlement-management-ciem",
            "https://www.wiz.io/academy/iam-security",
            "https://www.wiz.io/academy/effective-permissions",
            "https://www.wiz.io/academy/aws-iam-best-practices",
            "https://www.wiz.io/academy/ciem-vs-iam",
            "https://www.wiz.io/academy/identity-security-in-the-cloud",
            "https://www.wiz.io/academy/principle-of-least-privilege-polp",
            "https://www.wiz.io/academy/cloud-data-security",
            "https://www.wiz.io/academy/data-risk-assessment",
            "https://www.wiz.io/academy/data-security-posture-management-dspm",
            "https://www.wiz.io/academy/data-security-best-practices",
            "https://www.wiz.io/academy/sensitive-data-discovery",
            "https://www.wiz.io/academy/data-leakage",
            "https://www.wiz.io/academy/data-security-controls",
            "https://www.wiz.io/academy/best-native-aws-security-tools",
            "https://www.wiz.io/academy/aws-security-best-practices",
            "https://www.wiz.io/academy/azure-security-best-practices",
            "https://www.wiz.io/academy/azure-security-tools",
            "https://www.wiz.io/academy/azure-security-risks",
            "https://www.wiz.io/academy/aws-security-risks",
            "https://www.wiz.io/academy/google-cloud-security-best-practices",
            "https://www.wiz.io/academy/google-cloud-security-tools",
            "https://www.wiz.io/academy/kubernetes-security-best-practices",
            "https://www.wiz.io/academy/what-is-container-security",
            "https://www.wiz.io/academy/container-security-scanning",
            "https://www.wiz.io/academy/container-security-best-practices",
            "https://medium.com/@grpeto/building-secure-and-compliant-architectures-on-aws-189b57daca41",
            "https://medium.com/@AlexanderObregon/aws-compliance-and-governance-for-beginners-985bd92f52b9",
            "https://learn.drata.com/hubfs/Downloadables/Drata_Complete_Guide_Cybersecurity_Risk_Management_New.pdf?utm_source=linkedin&utm_medium=paidsocial&utm_campaign=20251017_legacy_to_modern_DG_all_ALL&utm_id=120232454249370099&utm_content=120232454249400099&utm_term=120232454249410099"
        ]
    },
    "devops": {
        "DEVOPS_DOCS": [
            "https://kubernetes.io/docs/home/",
            "https://www.redhat.com/rhdc/managed-files/ma-kubernetes-clusters-dummies-ebook-f26221-202011-en.pdf?sc_cid=RHCTE0230000222327&utm_medium=paid&utm_source=ig&utm_id=120214045400310692&utm_content=120218618891300692&utm_term=120214213442250692&utm_campaign=120214045400310692",
            "https://www.redhat.com/rhdc/managed-files/cl-oreilly-kubernetes-patterns-ebook-399085-202306-en.pdf?sc_cid=RHCTE0230000222327&utm_medium=paid&utm_source=ig&utm_id=120214045400310692&utm_content=120232116360990692&utm_term=120214213442250692&utm_campaign=120214045400310692",
            "https://docs.docker.com/",
            "https://helm.sh/docs/",
            "https://argo-cd.readthedocs.io/en/stable/",
            "https://circleci.com/docs/",
            "https://karpenter.sh/docs/",
            "https://docs.github.com/en/actions",
            "https://docs.github.com/en/actions",
            "https://www.jenkins.io/doc/",
            "https://docs.gitlab.com/ci/",
            "https://registry.terraform.io/browse/providers",
            "https://registry.terraform.io/browse/modules",
            "https://registry.terraform.io/browse/policies",
            "https://registry.terraform.io/browse/run-tasks",
            "https://developer.hashicorp.com/terraform/tutorials",
            "https://developer.hashicorp.com/terraform/tutorials",
            "https://docs.aws.amazon.com/cloudformation/",
            "https://www.pulumi.com/docs/",
            "https://docs.ansible.com/",
            "https://docs.chef.io/",
            "https://developer.hashicorp.com/vault/docs",
            "https://developer.hashicorp.com/nomad/docs",
            "https://developer.hashicorp.com/consul/docs",
            "https://developer.hashicorp.com/boundary/docs",
            "https://medium.com/@megaurav25/linkerd-step-by-step-2dfab7b00ff",
            "https://www.elastic.co/docs",
            "https://prometheus.io/docs/introduction/overview/",
            "https://docs.newrelic.com/",
            "https://docs.datadoghq.com/",
            "https://docs.dynatrace.com/docs?utm_source=bing&utm_medium=cpc&utm_term=dynatrace%20do",
            "https://grafana.com/docs/",
            "https://docs.aws.amazon.com/cdk/api/v2/",
            "https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-cloud/",
            "https://docs.datadoghq.com/",
            "https://docs.dynatrace.com/docs?utm_source=bing&utm_medium=cpc&utm_term=dynatrace%20do",
            "https://grafana.com/docs/",
            "https://docs.aws.amazon.com/cdk/api/v2/",
            "https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-cloud/",
            "https://support.atlassian.com/bitbucket-cloud/",
            "https://docs.ubuntu.com/",
            "https://www.kernel.org/doc/html/v4.10/index.html",

            "https://linuxconfig.org/linux-commands-tutorial",

            "https://devdocs.io/bash/",

            "https://www.python.org/doc/",

            "https://www.typescriptlang.org/docs/",

            "https://go.dev/doc/",

            "https://opentofu.org/docs/",

            "https://spinnaker.io/docs/",

            "https://docs.docker.com/engine/swarm/",

            "https://www.checkov.io/1.Welcome/Quick%20Start.html",

            "https://docs.snyk.io/discover-snyk/getting-started",

            "https://trivy.dev/docs/latest/",   

            "https://github.com/kubecost",

            "https://docs.aws.amazon.com/eks/latest/userguide/cost-monitoring-kubecost.html",

            "https://nginx.org/en/docs/",

            "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html",

            "https://www.elastic.co/guide/en/kibana/current/index.html",

            "https://www.elastic.co/guide/en/logstash/current/index.html",

            "https://www.elastic.co/guide/en/beats/current/index.html",

        ]
    }
}
