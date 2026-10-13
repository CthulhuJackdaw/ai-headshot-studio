package dev.ahs;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Path;
import java.util.List;

/** Submits batch headshot jobs to a running ai-headshot-studio HTTP bridge. */
public final class BatchClient {
    private final HttpClient http = HttpClient.newHttpClient();
    private final URI base;

    public BatchClient(URI base) { this.base = base; }

    public String submit(List<Path> refs, String style, int count) throws IOException, InterruptedException {
        String body = "{\"style\":\"" + style + "\",\"count\":" + count + "}";
        HttpRequest req = HttpRequest.newBuilder(base.resolve("/v1/jobs"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }
}