I am not original author of this code I simply modified the code by Andrew Brown
to work in the field of the integers mod 59. For the Original code see
https://github.com/brownan/Reed-Solomon

His README covers most of this. My changes include:
The polynomial class had some minor edits to make it work purely in the integers mod 59

b59conv -Base 59 converter- This function takes single characters and converts them into
an integer between 0 and 58. The alphabet that it accepts is
0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ
note that O, I, and l are excluded. This alphabet was chosen since it is used with
Bitcoin addresses these letters are excluded because they degrade readability.
The 0 is included as a "whitespace" type character. Leading zeros will be stripped
unless decode with nostrip=true is used. Generally its just advisable to avoid using this
character. It can easily be changed to whitespace by substituting 0 with "\0"

r59conv -Reverse base 59 converter- Performs the task of converting integers between
0 and 58 back into their corresponding characters.

These two functions take the place of ord and chr from the original code respectfully.

rstest was edited to make it work with the new framework.