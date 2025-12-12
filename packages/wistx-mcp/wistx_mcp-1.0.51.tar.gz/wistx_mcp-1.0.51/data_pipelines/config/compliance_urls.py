"""Compliance standards URL configuration.

This file contains URLs for all compliance standards.
Each standard can have multiple source URLs.
"""

COMPLIANCE_URLS = {
    "PCI-DSS": {
        "version": "4.0",
        "base_url": "https://www.pcisecuritystandards.org",
        "urls": [
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
        "expected_controls": 400,
    },
    "CIS": {
        "version": "2.0",
        "base_url": "https://www.cisecurity.org",
        "urls": {
            "aws": [
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
            "gcp": [
                "https://www.cisecurity.org/benchmark/google_cloud_platform",
                "https://www.cisecurity.org/benchmark/gcp",
                "https://databrackets.com/services/google-cloud-platform-gcp-security-assessment/",
                "https://www.clouddefense.ai/cis-benchmarks-for-google-cloud-platform/",
                "https://github.com/GoogleCloudPlatform/inspec-gcp-cis-benchmark",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Google_Cloud_Platform_Foundation_Benchmark_v1.0.0.pdf"
            ],
            "azure": [
                "https://www.cisecurity.org/benchmark/azure",
                "https://www.cisecurity.org/benchmark/microsoft_azure",
                "https://learn.microsoft.com/en-us/security/benchmark/azure/overview-v3",
                "https://learn.microsoft.com/en-us/security/benchmark/azure/overview-v2",
                "https://github.com/jonathanbglass/cis-benchmarks/blob/master/CIS_Microsoft_Azure_Foundations_Benchmark_v1.1.0.pdf"
            ],
        },
        "expected_controls": 200,
    },
    "HIPAA": {
        "version": "Security Rule",
        "base_url": "https://www.hhs.gov/hipaa",
        "urls": [
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
        "expected_controls": 53,
    },
    "SOC2": {
        "version": "2.0",
        "base_url": "https://www.aicpa.org",
        "urls": [
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
        "expected_controls": 60,
    },
    "NIST-800-53": {
        "version": "Rev 5",
        "base_url": "https://csrc.nist.gov",
        "urls": [
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
        "expected_controls": 900,
    },
    "ISO-27001": {
        "version": "2022",
        "base_url": "https://www.iso.org",
        "urls": [
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
        "expected_controls": 100,
    },
    "GDPR": {
        "version": "2018",
        "base_url": "https://gdpr.eu/",
        "urls": [
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
        "expected_controls": 378,
    },
    "FedRAMP": {
        "version": "Moderate Baseline",
        "base_url": "https://www.fedramp.gov",
        "urls": [
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
        "expected_controls": 325,
    },
    "CCPA": {
        "version": "2020",
        "base_url": "https://oag.ca.gov",
        "urls": [
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
        "expected_controls": 50,
    },
    "SOX": {
        "version": "2002",
        "base_url": "https://www.sec.gov",
        "urls": [
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
        "expected_controls": 40,
    },
    "GLBA": {
        "version": "1999",
        "base_url": "https://www.ftc.gov",
        "urls": [
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
        "expected_controls": 120,
    },
}
