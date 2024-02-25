# -= Thermal Conduction =-
- A thermal conduction simulation based on text or image. Really simplist physics modelisation for this simple simulation.
- I use a discrete analogue of the second derivative to modelise the Laplace operator, used in the thermal conduction law.
I also simplified the thermal conduction law, reducing it to a single factor.
![blurred cahun](https://github.com/EwannAnacombesque/Thermal-Conduction/assets/67865912/7c9bda61-1a36-4917-bd3b-4aced82adaf9)
![cahun usual](https://github.com/EwannAnacombesque/Thermal-Conduction/assets/67865912/baa21d5c-c261-4885-9fdd-a363ca5dcf88)

## Blank mode :
In blank mode, the canva is blank, it's all yours.
As it is in image mode, and text mode, you can hold **right click** to **cool** down the cells, and **left click** to **heat** up the cells.

## Image mode :
In this mode, the image is transformed into a *heatmap*.
The heat is determined by the red component of the image. This heat will spred all over the canva, resulting in a equivalent to a gaussian blur.
In fact, those applications are the same.

## Text mode :
In this mode, the text is transformed into a *pseudo-heatmap*.
The chars of the text are replaced by their ASCII codes, and those are converted in binary, and are casted back into string.

# -= Usage =-
- Use *main.py [-h] [-t [{blank,image,text}]] [-f [FILE]] [-c [COLOR]] [-dt [DT]]*

Specifications :
  -t [{blank,image,text}], --type [{blank,image,text}]
                        Type of heatmap preset
  
  -f [FILE], --file [FILE]
                        In case type is either image or text, specify the file path
  
  -c [COLOR], --color [COLOR]
                        Color accuracy of the canva, the size of the color palette
                        => Ideal *5* or *250*
  
  -dt [DT], --dt [DT]   Time modifier, and simulatoin accuracy modifier, the simulation is as good as dt is little, and as fast as dt is big
                        => Ideal dt <= 0.1
