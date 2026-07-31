{{/*
Application name
*/}}
{{- define "k8s-network-monitor.name" -}}
{{ .Chart.Name }}
{{- end }}


{{/*
Full resource name
*/}}
{{- define "k8s-network-monitor.fullname" -}}
{{ .Release.Name }}
{{- end }}