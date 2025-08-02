#include <imgui.h>
#include <fuzzy.h>  // ssdeep header

void hash_and_compare_gui() {
    static char file1[260] = "";
    static char file2[260] = "";
    static int similarity = -2;  // -2 = not computed, -1 = error

    ImGui::InputText("File 1", file1, 260);
    ImGui::InputText("File 2", file2, 260);

    if (ImGui::Button("Compare")) {
        char hash1[FUZZY_MAX_RESULT] = {0};
        char hash2[FUZZY_MAX_RESULT] = {0};
        int r1 = fuzzy_hash_filename(file1, hash1);
        int r2 = fuzzy_hash_filename(file2, hash2);

        if (r1 == 0 && r2 == 0) {
            similarity = fuzzy_compare(hash1, hash2);
        } else {
            similarity = -1;
        }
    }

    if (similarity >= 0) {
        ImGui::Text("Similarity: %d%%", similarity);
    } else if (similarity == -1) {
        ImGui::Text("Error reading files or computing hash");
    }
}
