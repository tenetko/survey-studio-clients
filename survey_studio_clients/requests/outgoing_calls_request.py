OUTGOING_CALLS_REQUEST = """
{{
  "callsExportType": 5,
  "allCallsFiltrationMode": 0,
  "from": "{date_from}",
  "to": "{date_to}",
  "projectId": {project_id},
  "assignedClientId": null,
  "operatorId": null,
  "callId": null,
  "phone": null,
  "minCallDuration": null,
  "talkDurationType": 0,
  "minTalkDuration": null,
  "maxTalkDuration": null,
  "callResult": null,
  "callResultGroup": null,
  "isPilot": null,
  "isListened": null,
  "operatorTalk": null,
  "hangupInitiator": null,
  "archiveSingleXlsxResultFile": true,
  "includeRecordFileName": null,
  "includeInterviewSuccessCounterMatch": null,
  "onlyWithRecords": null,
  "maxRowsInXlsxFile": null
}}
"""
