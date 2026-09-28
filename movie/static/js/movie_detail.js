// movie_detail.js : 영화 상세 페이지 전용 스크립트
// (템플릿의 {% block script %} 안에서 불러오므로 DOM이 모두 그려진 뒤에 실행됩니다)

// ----- 탭 전환 -----
document.querySelectorAll('.tab-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        document.querySelectorAll('.tab-btn').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        document.querySelectorAll('.tab-panel').forEach(function (p) { p.style.display = 'none'; });
        document.getElementById('tab-' + btn.dataset.tab).style.display = 'block';
    });
});

// ----- 예고편 팝업 (HTML의 onclick="openTrailer(...)" 에서 호출하므로 전역 함수로 둬야 함) -----
function openTrailer(url) {
    window.open(
        url,
        'trailerWindow',
        'width=1000,height=600,resizable=yes,scrollbars=yes'
    );
}

// ----- 관람평 작성 후 돌아왔을 때 관람평 탭 자동 열기 -----
if (window.location.hash === '#tab-review') {
    document.querySelector('.tab-btn[data-tab="review"]').click();
}

// ----- 트레일러 슬라이더 -----
const trailerTrack = document.querySelector('.trailer-track');
const trailerItems = document.querySelectorAll('.trailer-item');
const trailerPrev = document.getElementById('trailer-prev');
const trailerNext = document.getElementById('trailer-next');
let trailerIndex = 0;

if (trailerTrack && trailerItems.length > 3) {
    function moveTrailer() {
        const itemWidth = trailerItems[0].offsetWidth + 16;
        trailerTrack.style.transform = `translateX(-${trailerIndex * itemWidth}px)`;
    }

    trailerNext.addEventListener('click', function () {
        trailerIndex++;
        if (trailerIndex > trailerItems.length - 3) {
            trailerIndex = 0;
        }
        moveTrailer();
    });

    trailerPrev.addEventListener('click', function () {
        trailerIndex--;
        if (trailerIndex < 0) {
            trailerIndex = trailerItems.length - 3;
        }
        moveTrailer();
    });

    window.addEventListener('resize', moveTrailer);
}

// ----- 스틸컷 더보기 -----
var stillMoreBtn = document.getElementById('stillMoreBtn');
if (stillMoreBtn) {
    stillMoreBtn.addEventListener('click', function () {
        document.querySelectorAll('#stillGallery .still-hidden').forEach(function (img) {
            img.classList.remove('still-hidden');
        });
        stillMoreBtn.style.display = 'none';
    });
}

// ----- 좋아요 (서버에 저장) -----
var likeTag = document.getElementById('likeTag');
var likeCount = document.getElementById('likeCount');
if (likeTag) {
    likeTag.addEventListener('click', function () {
        fetch('/movie/' + likeTag.dataset.movieId + '/like', { method: 'POST' })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                likeCount.textContent = data.like_count;
                likeTag.classList.add('flash');
                setTimeout(function () {
                    likeTag.classList.remove('flash');
                }, 250);
            })
            .catch(function (err) {
                console.error('좋아요 요청 실패:', err);
            });
    });
}

// ----- 링크 복사 -----
var copyLinkBtn = document.getElementById('copyLinkBtn');
var copyToast = document.getElementById('copyToast');

if (copyLinkBtn) {
    copyLinkBtn.addEventListener('click', function () {
        var url = window.location.href;

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(showToast).catch(fallbackCopy);
        } else {
            fallbackCopy();
        }

        function fallbackCopy() {
            var temp = document.createElement('textarea');
            temp.value = url;
            temp.style.position = 'fixed';
            temp.style.opacity = '0';
            document.body.appendChild(temp);
            temp.select();
            document.execCommand('copy');
            document.body.removeChild(temp);
            showToast();
        }

        function showToast() {
            copyToast.classList.add('show');
            setTimeout(function () {
                copyToast.classList.remove('show');
            }, 1800);
        }
    });
}
