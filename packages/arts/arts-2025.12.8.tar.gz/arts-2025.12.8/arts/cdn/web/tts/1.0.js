"use strict";

class Multi_tts {
    constructor() {
        this.languages = {
            '英': { lang: 'en-GB', voice: null, search_count: 0 },
            '美': { lang: 'en-US', voice: null, search_count: 0 },
            '普': { lang: 'zh-CN', voice: null, search_count: 0 },
            '日': { lang: 'ja-JP', voice: null, search_count: 0 },
        }
    }

    async speak(text, lang_mark = '普', rate = 1.0, clear_speech_queue = false) {
        /*
        rate推荐值：
            英：1.1
            美：1.1
            普：1.0
            日：0.9
        */
        let language = this.languages[lang_mark]
        if ((!language['voice']) && (language['search_count'] < 5)) {
            language['search_count'] += 1
            let lang = language['lang']
            for (let voice of window.speechSynthesis.getVoices()) {
                if (voice.lang.startsWith(lang) && voice.name.toLowerCase().includes('natural')) {
                    language['voice'] = voice
                    break
                }
            }
        }
        let voice = language['voice']
        let utterance = new SpeechSynthesisUtterance(text)
        utterance.lang = language.lang
        utterance.rate = Math.min(Math.max(rate, 0.5), 2)
        utterance.volume = 1
        if (voice) {
            utterance.voice = voice
        }
        return new Promise((resolve, reject) => {
            utterance.onend = () => resolve({})
            utterance.onerror = (event) => {
                console.log(`朗读失败 | ${text} | ${event.error}`)
                resolve({})  // 标记完成
            }
            if (clear_speech_queue) {
                window.speechSynthesis.cancel()
            }
            window.speechSynthesis.speak(utterance)
        })
    }
}

window.tts = new Multi_tts()
