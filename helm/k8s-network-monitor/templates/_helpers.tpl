{{/*
Chart name.
*/}}
{{- define "k8s-network-monitor.name" -}}
{{ .Chart.Name }}
{{- end }}


{{/*
Full resource name.
*/}}
{{- define "k8s-network-monitor.fullname" -}}
{{ .Release.Name }}
{{- end }}


{{/*
Common Kubernetes labels.
*/}}
{{- define "k8s-network-monitor.labels" -}}
helm.sh/chart: {{ include "k8s-network-monitor.name" . }}
app.kubernetes.io/name: {{ include "k8s-network-monitor.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}