#define UNICODE
#define _UNICODE

#include <windows.h>                      // Win32 API
#include <gl/GL.h>                        // OpenGL headers
#include "imgui.h"                        // Core ImGui
#include "imgui_impl_win32.h"            // ImGui Win32 binding
#include "imgui_impl_opengl3.h"          // ImGui OpenGL3 binding

// 👇 Forward declarations
LRESULT CALLBACK WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

// 📌 Globals
HDC hDC;
HGLRC hGLRC;

// 🧠 Entry point
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int) {

    // 🔲 Step 1: Register window class
    WNDCLASS wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"ImGuiExampleClass";
    RegisterClass(&wc);

    // 🔳 Step 2: Create window
    HWND hWnd = CreateWindowEx(
        0,
        wc.lpszClassName,
        L"Fuzzy Scanner",
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT,
        800, 600,
        NULL, NULL, hInstance, NULL
    );

    // ⚙️ Step 3: Set up OpenGL context
    hDC = GetDC(hWnd);
    PIXELFORMATDESCRIPTOR pfd = {
        sizeof(PIXELFORMATDESCRIPTOR), 1,
        PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER,
        PFD_TYPE_RGBA, 32, 0,0,0,0,0,0,0,0,0,0,0,0,0,
        24, 8, 0, PFD_MAIN_PLANE, 0, 0, 0, 0
    };
    int pf = ChoosePixelFormat(hDC, &pfd);
    SetPixelFormat(hDC, pf, &pfd);
    hGLRC = wglCreateContext(hDC);
    wglMakeCurrent(hDC, hGLRC);

    // 🚀 Step 4: Initialize ImGui
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    ImGui_ImplWin32_Init(hWnd);
    ImGui_ImplOpenGL3_Init();

    // 🌙 Optional: Style
    ImGui::StyleColorsDark();

    // 🔁 Step 5: Main loop
    MSG msg = {};
    while (msg.message != WM_QUIT) {
        // Handle Win32 messages
        if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
            continue;
        }

        // Clear screen
        glViewport(0, 0, 800, 600);
        glClearColor(0.1f, 0.12f, 0.15f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // Start ImGui frame
        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplWin32_NewFrame();
        ImGui::NewFrame();

        // 🎨 Build UI
        ImGui::Begin("Fuzzy Scanner");
        ImGui::Text("Welcome to your first GUI!");
        ImGui::End();

        // Render UI
        ImGui::Render();
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        // Show result
        SwapBuffers(hDC);
    }

    // 🧹 Step 6: Cleanup
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();

    wglMakeCurrent(NULL, NULL);
    wglDeleteContext(hGLRC);
    ReleaseDC(hWnd, hDC);
    DestroyWindow(hWnd);
    UnregisterClass(wc.lpszClassName, hInstance);

    return 0;
}

// 📨 Handles all Win32 messages
extern LRESULT ImGui_ImplWin32_WndProcHandler(HWND, UINT, WPARAM, LPARAM);

LRESULT CALLBACK WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
    return true;

    switch (msg) {
        case WM_SIZE:
            // You can handle resizing if needed
            break;
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
    }
    return DefWindowProc(hWnd, msg, wParam, lParam);
}
