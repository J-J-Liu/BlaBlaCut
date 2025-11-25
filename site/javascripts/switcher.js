document.addEventListener("DOMContentLoaded", function() {
    const path = window.location.pathname;

    // --- 0. 检测主页并添加类名 (保持不变) ---
    if (path === "/" || path === "/index.html" || path.endsWith("/index") || path.endsWith("/index.html")) {
        document.body.classList.add("is-home-page");
    }

    // --- 0.1. 检测 notes_repo 下的页面并添加类名 ---
    if (path.includes("/notes_repo/")) {
        document.body.classList.add("is-notes-repo-page");
    }

    // --- 1. 自动恢复滚动位置逻辑 (保持不变) ---
    const storageKey = "scroll_pos_" + path;
    const savedPosition = sessionStorage.getItem(storageKey);

    if (savedPosition) {
        setTimeout(() => {
            window.scrollTo({
                top: parseInt(savedPosition),
                behavior: "instant"
            });
        }, 100);
    }

    // --- 2. 按钮生成逻辑 ---
    const KEY_PAPER = "paper_notes";
    const KEY_FIGS = "figs_notes";
    const KEY_ELI5 = "ELI5_notes";

    const pageConfigs = {
        [KEY_PAPER]: {
            name: "阅读笔记",
            icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-9 13H7v-2h2v2zm0-4H7v-2h2v2zm0-4H7V5h2v2zm6 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V5h2v2z"/></svg>'
        },
        [KEY_FIGS]: {
            name: "图表分析",
            icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2v-3h2v3zm4 0h-2v-5h2v5z"/></svg>'
        },
        [KEY_ELI5]: {
            name: "ELI5详解",
            icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z"/></svg>'
        }
    };

    // --- 修改重点 1: 更精准的当前页面检测 ---
    // 即使父目录叫 paper_notes，如果当前文件名是 figs_notes，我们也应该识别为 figs_notes
    // 方法：比较这三个词在路径中最后一次出现的位置，位置最靠后（索引最大）的才是真正的当前文件名。
    const keys = [KEY_PAPER, KEY_FIGS, KEY_ELI5];
    let currentPageKey = null;
    let maxIndex = -1;

    keys.forEach(key => {
        // 查找该 key 在 path 中最后出现的位置
        const index = path.lastIndexOf(key);
        // 如果找到了，并且位置比之前的更靠后（说明它是文件名，而不是父文件夹名）
        if (index > maxIndex) {
            maxIndex = index;
            currentPageKey = key;
        }
    });

    // 如果三个都没找到，说明不在这些页面，直接返回
    if (!currentPageKey) return; 

    // --- 修改重点 1 结束 ---

    const otherPages = Object.keys(pageConfigs).filter(key => key !== currentPageKey);

    const btnContainer = document.createElement("div");
    btnContainer.className = "paper-switch-btn-container";
    document.body.appendChild(btnContainer);

    otherPages.forEach((targetKey, index) => {
        const targetConfig = pageConfigs[targetKey];

        // --- 修改重点 2: 只替换最后一部分 ---
        // 既然我们已经确定 currentPageKey 是最后出现的那一个（在 maxIndex 位置）
        // 我们就精准地只把那一块切掉，换成新的 key
        let targetUrl = path.substring(0, maxIndex) + 
                        targetKey + 
                        path.substring(maxIndex + currentPageKey.length);
        
        // 防止 .html 结尾的文件被错误追加 /
        if (!targetUrl.endsWith('/') && !targetUrl.endsWith('.html')) {
            targetUrl += '/';
        }

        const btn = document.createElement("a");
        btn.className = "paper-switch-btn";
        btn.innerHTML = targetConfig.icon + "<span>" + targetConfig.name + "</span>";
        btn.style.cursor = "pointer";

        // --- 3. 点击按钮时的保存逻辑 ---
        btn.addEventListener("click", function(e) {
            e.preventDefault(); 
            sessionStorage.setItem(storageKey, window.scrollY);
            window.location.href = targetUrl;
        });

        btnContainer.appendChild(btn);
    });
});