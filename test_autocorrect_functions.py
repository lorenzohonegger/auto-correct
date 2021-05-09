import pytest
from autocorrect_functions import (process_data, get_count, get_probs, delete_letter, switch_letter, 
                                   replace_letter, insert_letter, edit_one_letter, edit_two_letters, get_corrections)

@pytest.mark.parametrize(("input_words, output_words"), 
                         [({'hello', 'my'}, {'my': 1, 'hello': 1}), 
                         ({'hello', 'my', 'hello'}, {'my': 1, 'hello': 1}),
                          (['hello', 'my', 'hello'], {'my': 1, 'hello': 1})])
def test_get_count(input_words, output_words):
    assert output_words == get_count(input_words)
    
    
    
@pytest.mark.parametrize(("input_words, output_words"), 
                         [({'my': 1, 'hello': 1}, {'my': 0.5, 'hello': 0.5}),
                          ({'my': 3, 'hello': 1}, {'my': 0.75, 'hello': 0.25})])
def test_get_probs(input_words, output_words):
    assert output_words == get_probs(input_words)
    
@pytest.mark.xfail(raises=TypeError)
@pytest.mark.parametrize(("input_words, "), 
                         [("string1"), (12), ([1, 2, 3])])
def test_get_probs_arguments(input_words):
    get_probs(input_words)

    
    
@pytest.mark.parametrize(("input_word, output_words"), 
                         [('hello', {'ello', 'hllo', 'helo', 'helo', 'hell'}),
                          ('my', {'y', 'm'})])
def test_delete_letter(input_word, output_words):
    assert output_words == set(delete_letter(input_word))


@pytest.mark.parametrize(("input_word, output_words"), 
                         [('hello', {'ehllo', 'hello', 'helol', 'hlelo'}),
                          ('my', {'ym'})])
def test_switch_letter(input_word, output_words):
    assert output_words == set(switch_letter(input_word))
    
@pytest.mark.parametrize(("input_word, output_words"), 
                         [('my', {'yy', 'ky', 'mm', 'md', 'sy', 'me', 'fy', 'mt', 'jy', 'cy', 'mw', 'mx', 'mg', 'zy', 'ly', 'mo', 'mb', 'ml', 'hy', 'mr', 'gy', 'dy', 'ey', 'ma', 'mh', 'ty', 'qy', 'mj', 'uy', 'mz', 'ay', 'mu', 'ry', 'by', 'mp', 'py', 'mf', 'vy', 'wy', 'iy', 'mi', 'oy', 'xy', 'ms', 'mn', 'mv', 'ny', 'mq', 'mk', 'mc'})])
def test_replace_letter(input_word, output_words):
    assert output_words == set(replace_letter(input_word))
    
    
@pytest.mark.parametrize(("input_word, output_words"), 
                         [('my', {'mpy', 'myw', 'myg', 'pmy', 'myp', 'myt', 'amy', 'qmy', 'rmy', 'lmy', 'myi', 'myo', 'mey', 'mxy', 'imy', 'may', 'mzy', 'hmy', 'mcy', 'myd', 'mty', 'mly', 'myf', 'myk', 'mby', 'emy', 'mjy', 'myl', 'mye', 'ymy', 'myy', 'muy', 'mqy', 'myr', 'omy', 'kmy', 'myj', 'myq', 'wmy', 'tmy', 'myu', 'mvy', 'cmy', 'jmy', 'myh', 'umy', 'mys', 'bmy', 'miy', 'mwy', 'msy', 'mfy', 'gmy', 'fmy', 'mny', 'myc', 'moy', 'myb', 'myx', 'zmy', 'mhy', 'vmy', 'mym', 'dmy', 'mmy', 'mya', 'mgy', 'nmy', 'xmy', 'mdy', 'mry', 'myn', 'mky', 'smy', 'myz', 'myv'})])
def test_insert_letter(input_word, output_words):
    assert output_words == set(insert_letter(input_word))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    