import React, { useEffect, useState } from "react";
import { SafeAreaView, View, Text, TextInput, Button, StyleSheet, Platform } from "react-native";
import { StatusBar } from "expo-status-bar";

const DEFAULT_BACKEND_URL = "http://localhost:5001";

export default function App() {
  const [backendUrl, setBackendUrl] = useState(DEFAULT_BACKEND_URL);
  const [healthStatus, setHealthStatus] = useState("unknown");
  const [lastError, setLastError] = useState("");

  const checkHealth = async () => {
    try {
      setLastError("");
      const res = await fetch(`${backendUrl}/health`);
      const json = await res.json();
      setHealthStatus(json.status || "ok");
    } catch (e) {
      setHealthStatus("error");
      setLastError(String(e));
    }
  };

  useEffect(() => {
    // Try once on load
    void checkHealth();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      <Text style={styles.title}>HomeStock Mobile</Text>
      <Text style={styles.subtitle}>
        React Native client for the existing FastAPI backend.
      </Text>

      <View style={styles.section}>
        <Text style={styles.label}>Backend URL</Text>
        <TextInput
          style={styles.input}
          value={backendUrl}
          onChangeText={setBackendUrl}
          autoCapitalize="none"
          autoCorrect={false}
        />
        <Text style={styles.help}>
          Example: http://192.168.1.10:5001 (desktop running the backend on your LAN)
        </Text>
      </View>

      <View style={styles.section}>
        <Button title="Check Backend Health" onPress={checkHealth} />
        <Text style={styles.statusLabel}>Health status: {healthStatus}</Text>
        {lastError ? <Text style={styles.errorText}>{lastError}</Text> : null}
      </View>

      <View style={styles.section}>
        <Text style={styles.noteTitle}>How this works</Text>
        <Text style={styles.noteText}>
          This mobile app talks to the same FastAPI backend you already run for the
          Electron app. Run the backend on a desktop or server, make sure your iPad
          or Android device is on the same network, and point the URL above to that machine.
        </Text>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          Platform: {Platform.OS} — backend remains Python FastAPI.
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: "#0f172a",
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "#e5e7eb",
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: "#9ca3af",
    marginBottom: 16,
  },
  section: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    color: "#e5e7eb",
    marginBottom: 4,
  },
  input: {
    backgroundColor: "#111827",
    borderRadius: 6,
    paddingHorizontal: 10,
    paddingVertical: 8,
    color: "#e5e7eb",
    borderWidth: 1,
    borderColor: "#374151",
  },
  help: {
    fontSize: 12,
    color: "#9ca3af",
    marginTop: 4,
  },
  statusLabel: {
    marginTop: 8,
    fontSize: 14,
    color: "#e5e7eb",
  },
  errorText: {
    marginTop: 4,
    fontSize: 12,
    color: "#f97373",
  },
  noteTitle: {
    fontSize: 14,
    fontWeight: "600",
    color: "#e5e7eb",
    marginBottom: 4,
  },
  noteText: {
    fontSize: 13,
    color: "#d1d5db",
  },
  footer: {
    marginTop: "auto",
    borderTopWidth: 1,
    borderTopColor: "#1f2937",
    paddingTop: 8,
  },
  footerText: {
    fontSize: 12,
    color: "#6b7280",
    textAlign: "center",
  },
});


