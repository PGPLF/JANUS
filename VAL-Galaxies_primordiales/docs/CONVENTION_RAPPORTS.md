# Convention de Nommage des Rapports
**Version**: 1.0
**Date**: 2026-01-07

---

## Convention Standard

### Format général
```
RPT-{TYPE}_{PHASE}_{VERSION}.md
```

### Types de rapports

| Type | Description | Exemple |
|------|-------------|---------|
| `AUDIT` | Rapport d'audit/validation | RPT-AUDIT_Phase3_v1.md |
| `EXEC` | Rapport d'exécution | RPT-EXEC_Phase1_v1.md |
| `DATA` | Rapport sur les données | RPT-DATA_Quality_v1.md |

### Phases

| Phase | Code |
|-------|------|
| Phase 1 | `Phase1` |
| Phase 2 | `Phase2` |
| Phase 3.0 | `Phase3.0` |
| Phase 3.1 | `Phase3.1` |
| Phase 3.2 | `Phase3.2` |
| Phase 3.3 | `Phase3.3` |
| Phase 3 (complet) | `Phase3` |

---

## Mapping Ancien → Nouveau

| Fichier Ancien | Fichier Nouveau | Statut |
|----------------|-----------------|--------|
| RPT-EXECUTION_Phase1.md | RPT-EXEC_Phase1_v4.md | À renommer |
| RPT-AUDIT_FINAL_v4.md | RPT-AUDIT_Phase2_FINAL.md | À renommer |
| AUDIT_PHASE2_RAPPORT.md | **ARCHIVER** | Doublon |
| PHASE2_AUDIT_REPORT.md | **ARCHIVER** | Doublon |
| RPT_PHASE2_VALIDATION.md | **ARCHIVER** | Doublon |
| AUDIT_REPORT_3.0a.md | RPT-AUDIT_Phase3.0a_v1.md | À renommer |
| RPT_PHASE32_JANUS.md | RPT-EXEC_Phase3.2_JANUS_v1.md | À renommer |
| RPT_PHASE33_LCDM.md | RPT-EXEC_Phase3.3_LCDM_v1.md | À renommer |
| RPT_PHASE3_v2.md | RPT-EXEC_Phase3_v2.md | À renommer |
| RPT-AUDIT_Phase3_v1.md | **CONSERVER** | Nouveau |

---

## Rapports Officiels par Phase

### Phase 1
- **Audit**: RPT-AUDIT_Phase1_v4.md (à créer depuis RPT-EXECUTION_Phase1.md)

### Phase 2
- **Audit**: RPT-AUDIT_Phase2_FINAL.md

### Phase 3
- **Audit**: RPT-AUDIT_Phase3_v1.md (ACTUEL - identifie problèmes critiques)
- **Exécution**: RPT-EXEC_Phase3_v2.md (résultats - À CORRIGER)

---

## Actions de Nettoyage

```bash
# 1. Archiver les doublons
mkdir -p docs/archives/reports_legacy
mv AUDIT_PHASE2_RAPPORT.md docs/archives/reports_legacy/
mv PHASE2_AUDIT_REPORT.md docs/archives/reports_legacy/
mv PHASE2_REPORT.md docs/archives/reports_legacy/
mv PHASE3_AUDIT_REPORT.md docs/archives/reports_legacy/
mv RPT_PHASE2_VALIDATION.md docs/archives/reports_legacy/
mv RPT_PHASE3_COMPLETE.md docs/archives/reports_legacy/
mv RPT_PHASE3_FINAL.md docs/archives/reports_legacy/

# 2. Renommer les rapports officiels
mv RPT-EXECUTION_Phase1.md RPT-EXEC_Phase1_v4.md
mv RPT-AUDIT_FINAL_v4.md RPT-AUDIT_Phase2_FINAL.md
mv AUDIT_REPORT_3.0a.md RPT-AUDIT_Phase3.0a_v1.md
mv RPT_PHASE32_JANUS.md RPT-EXEC_Phase3.2_JANUS_v1.md
mv RPT_PHASE33_LCDM.md RPT-EXEC_Phase3.3_LCDM_v1.md
mv RPT_PHASE3_v2.md RPT-EXEC_Phase3_v2.md
```

---

*Convention établie pour assurer la traçabilité des rapports*
