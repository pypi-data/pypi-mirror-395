\version "2.25.24"
\paper{
    indent=0\mm
    line-width=120\mm
    oddFooterMarkup=##f
    oddHeaderMarkup=##f
    bookTitleMarkup = ##f
    scoreTitleMarkup = ##f
    }
\score {
{% if false %}{# % if sng.scores_chords % #}
  <<
  \new ChordNames {
    \set chordChanges = ##f
    \set chordNameExceptions = #chExceptions
    \override ChordName #'font-size = #-1
    \chordmode {
  \set majorSevenSymbol = \markup { "Maj7" }
  \override ParenthesesItem #'font-size = #0
  {sng.scores_chords}
  } }
{% endif %}
\new GrandStaff <<
  \new Staff = "SA" <<
    \new Voice = "soprano" {
    {% if sng.scores_tempo %} \tempo {{sng.scores_tempo}} {% endif %}
    {% if sng.scores_alto %} \voiceOne {% endif %} <<
      {{sng.scores_preamble}} \relative g' {
      {{sng.scores_soprano}}
      } >> }
  {% if sng.scores_alto %}
   \new Voice = "alto" { \voiceTwo <<
     {{sng.scores_preamble}} \relative g' {
     {{sng.scores_alto}} }
   >> }
  {% endif %}
 >>

{% for lyrics in sng.get_lyrics() %}
\new Lyrics
\lyricsto "soprano" {
  {% if sng.other_font and not loop.first %}
  \override LyricText . font-shape = #'italic
  \override LyricText . font-family = #'sans
  \override LyricText . font-size = #-1
  {% endif %}
  {{lyrics}}
}
{% endfor %}

{% if sng.scores_tenor or sng.scores_bass %}
 \new Staff = "TB" <<
  \clef bass
  {% if sng.scores_tenor %}
  \new Voice = "tenor" {
    {% if sng.scores_bass %} \voiceOne {% endif %}
  << {{sng.scores_preamble}} \relative f {
    {{sng.scores_tenor}}
  } >> }
  {% endif %}
  {% if sng.scores_bass %}
  \new Voice = "bass" {
    \voiceTwo
    << {{sng.scores_preamble}} \relative f {
    {{sng.scores_bass}}
  } >> }
  {% endif %}
 >>
{% endif %}

>>

   \layout{
   {# setting font-name here causes italic above to not work
   See https://jane.mylino.net/#/api/comments/Comments/18890
   #}
   \context { \Lyrics \override LyricText.font-name = #"sans" }
   \context { \Score \omit BarNumber }
}
{% if sng.scores_chords %}
>>
{% endif %}

}
