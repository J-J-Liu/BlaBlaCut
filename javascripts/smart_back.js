document.addEventListener("DOMContentLoaded", function() {
    // === 配置区域 ===
    // 你的 "黄页" 路径关键词
    const COLLECTION_PATH = '/collections/';
    // 你的 "笔记" 路径关键词
    const NOTES_PATH = '/notes_repo/';
    // 存储在浏览器中的键名
    const STORE_URL_KEY = 'last_collection_url';
    const STORE_SCROLL_KEY = 'last_collection_scroll';
    const FLAG_RETURNING = 'is_returning_from_note';

    const currentUrl = window.location.href;

    // === 逻辑 A: 如果当前在 Collections 页面 ===
    if (currentUrl.includes(COLLECTION_PATH)) {
        // 1. 记录当前 URL 为 "最后访问的 Collection"
        sessionStorage.setItem(STORE_URL_KEY, currentUrl);

        // 2. 监听滚动，离开页面前保存滚动位置
        window.addEventListener('beforeunload', function() {
            sessionStorage.setItem(STORE_SCROLL_KEY, window.scrollY);
        });

        // 3. 检查是否是刚从 Note 点击图标返回的，如果是，恢复滚动位置
        if (sessionStorage.getItem(FLAG_RETURNING) === 'true') {
            const savedScroll = sessionStorage.getItem(STORE_SCROLL_KEY);
            if (savedScroll) {
                // 稍微延迟以确保页面渲染完成
                setTimeout(() => {
                    window.scrollTo(0, parseInt(savedScroll));
                }, 100); 
            }
            // 清除标记，以免刷新页面时乱跳
            sessionStorage.removeItem(FLAG_RETURNING);
        }
    }

    // === 逻辑 B: 如果当前在 Notes 页面，修改 Logo 行为 ===
    if (currentUrl.includes(NOTES_PATH)) {
        // 适配 Material for MkDocs 主题的 Logo 选择器
        // 如果你用的是其他主题，可能需要修改这里，例如 '.navbar-brand'
        const logoLink = document.querySelector('.md-header__button.md-logo'); 
        
        if (logoLink) {
            logoLink.addEventListener('click', function(e) {
                const lastCollection = sessionStorage.getItem(STORE_URL_KEY);
                
                // 只有当存有记录时才拦截
                if (lastCollection) {
                    e.preventDefault(); // 阻止默认回到主页的行为
                    
                    // 标记这是由于点击图标返回的（用于触发滚动恢复）
                    sessionStorage.setItem(FLAG_RETURNING, 'true');
                    
                    // 跳转
                    window.location.href = lastCollection;
                }
                // 如果没有记录（比如直接打开了笔记链接），则保持默认行为（回主页）
            });
        }
    }
});