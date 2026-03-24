    document.addEventListener('DOMContentLoaded', function() {
        var typewriterElements = document.querySelectorAll('.typewriter-title');
        typewriterElements.forEach(function(el) {
            var text = el.getAttribute('data-text');
            var textSpan = el.querySelector('.typewriter-text');
            var cursor = el.querySelector('.typewriter-cursor');
            if (text && textSpan) {
                var i = 0;
                var typeInterval = setInterval(function() {
                    if (i < text.length) {
                        textSpan.textContent += text.charAt(i);
                        i++;
                    } else {
                        clearInterval(typeInterval);
                        setTimeout(function() {
                            if (cursor) cursor.style.display = 'none';
                        }, 2000);
                    }
                }, 100);
            }
        });
    });
    
    // 日历交互函数 - 无刷新切换
    let currentYear = new Date().getFullYear();
    let currentMonth = new Date().getMonth() + 1;
    
    function changeMonth(year, month, delta) {
        month += delta;
        if (month > 12) {
            year++;
            month = 1;
        } else if (month < 1) {
            year--;
            month = 12;
        }
        currentYear = year;
        currentMonth = month;
        loadCalendar(year, month);
    }
    
    function selectDate(year, month, day) {
        // 只高亮选中的日期，不刷新页面
        document.querySelectorAll('.calendar-table td').forEach(td => {
            td.classList.remove('selected');
        });
        event.currentTarget.classList.add('selected');
    }
    
    function loadCalendar(year, month) {
        fetch('/api/calendar?year=' + year + '&month=' + month)
            .then(res => res.text())
            .then(html => {
                document.getElementById('calendar').outerHTML = html;
            });
    }
    </script>
    highlight_js = '''<script>
        // Initialize highlight.js for code blocks
        if (typeof hljs !== 'undefined') {
            hljs.highlightAll();
        }
    </script>'''
    extra_js = '''<script>
    // 初始化追加页面
    console.log('Append page JS starting...');
    
    function initAppendPage() {
        console.log('initAppendPage called, Quill status:', typeof Quill);
        
        if (typeof Quill === 'undefined') {
            console.log('Quill not loaded yet, retrying in 100ms...');
            setTimeout(initAppendPage, 100);
            return;
        }
        
        console.log('Quill is ready, initializing editor...');
        
        // 获取DOM元素
        var editorEl = document.getElementById('editor');
