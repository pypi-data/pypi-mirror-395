
import sys
import pathlib

BASEDIR = pathlib.Path(__file__).parent.resolve()
sys.path.append(str(BASEDIR / '..' / 'src'))

import fondi


class TestMethods:

    def run(self):
        [eval('TestMethods().{}()'.format(i)) for i in dir(self) if 'test' in i]

    def __createMathText__(self, mathtext, filename, fontsize=50, color=(255,255,255,255)):
        txt = fondi.MathText(mathtext, fontsize, color)
        txt.image.save(BASEDIR / filename)
        

    def testPolynomen(self):
        self.__createMathText__('2*x_{5}^{2}+7^{2}_{1}', 'images/polynomen.png')

    def testCases(self):
        self.__createMathText__('f(x^2)=\\cases{2*x}{10>x}{[2^{x}]}{10<x}{\\frac{1}{2}}{\\text{else}}', 'images/cases.png')
    
    def testNestedFraction(self):
        self.__createMathText__('10+\\frac{\\frac{1}{2}}{x}', 'images/nested_fraction.png')

    def testBigFont(self):
        self.__createMathText__('f(x^2)=\\cases{2*x}{10>x}{[2^{x}]}{10<x}{\\frac{1}{2}}{\\text{else}}', 'images/bigfont.png', 200)
    
    def testSmallFont(self):
        self.__createMathText__('f(x^2)=\\cases{2*x}{10>x}{[2^{x}]}{10<x}{\\frac{1}{2}}{\\text{else}}', 'images/smallfont.png', 16)

    def testSuperSuber(self):
        self.__createMathText__('0,4x^{3}+2*x^{2}+5*x_{n-1}+b_{a}+c_{0}+5^{2}_{x}', 'images/supersub.png')
    
    def testrsquared(self):
        self.__createMathText__('R^2=0,9281', 'images/rsquared.png')

    def testrsquared(self):
        self.__createMathText__('R^2=0,9281', 'images/rsquared.png')
    
    def testSquareRoot(self):
        self.__createMathText__('\\sqrt{10^{2+1}}', 'images/sqrt.png')
    
    def testSomethingCrazy(self):
        self.__createMathText__('\\sin(\\frac{x^2 + (10+2)_{hej}}{\\frac{2}{x}_{i,j}})', 'images/para.png')

    def testIntegral(self):
        self.__createMathText__('5x+\\int{2x}{dx} + 7x \\int{x^2}{dx}_{-2}^{2}', 'images/integral.png')
        self.__createMathText__('\\int_{-2}^{2} x^2 dx + \\int_a^b x dx', 'images/integral2.png')
        self.__createMathText__('\\int 3 \\sqrt{x} + e^{3 x} dx', 'images/integral3.png')
        self.__createMathText__('\\text{Bestem }\\int 3 \\sqrt{x} + e^{3 x} dx\\text{}', 'images/integral4.png')


    def testSpaces(self):
        self.__createMathText__('100\\quad000', 'images/10000a.png')
        self.__createMathText__('100\\,000', 'images/10000b.png')
        self.__createMathText__('100\\:000', 'images/10000c.png')
        self.__createMathText__('100\\;000', 'images/10000d.png')
        self.__createMathText__('100\\smallSpace000', 'images/10000e.png')
        self.__createMathText__('100\\qquad000', 'images/10000f.png')

    def test18x(self):
        self.__createMathText__('18x+\\ln{2 \\cdot x}', 'images/18x.png')
    
    def testRandomError(self):
        self.__createMathText__('(x^2-9)\\cdot (x+4)=0', 'images/error2.png')

    def testcauchysIntegralFormula(self):
        self.__createMathText__('f(z_0)=\\frac{1}{2 \\pi i}\\oint{\\frac{f(z)}{z-z_0}}{\\text{d}z}_{C}', 'images/cauchyesintegralformula.png')
        #self.__createMathText__('\\oint{\\frac{f(z)}{z-z_0}}{\\text{d}z}_{C}', 'images/cauchyesintegralformula.png')

    def testPara(self):
        self.__createMathText__("f'(x_0)+f(x_0)+\\int{f(x_0)}{dx}", 'images/paras.png')
        self.__createMathText__("f\\prime \\left(x_0 \\right)+f(x_0)+\\int{f(x_0)}{\\differentialD x}", 'images/parasleftright.png')


    def testDotAndTilde(self):
        self.__createMathText__("\\dot{x} + \\ddot{y} + \\tilde{z} + \\bar{a}", 'images/dot_tilde_bar.png')
        self.__createMathText__("\\dot{\\dot{x}} + a_{\\tilde{k_v}} + \\tilde{z} + \\bar{a}", 'images/dot_tilde_bar_2.png')


    def testSubscriptMultipleCharacters(self):
        self.__createMathText__('a_{ijk} + b^{xyz} + c_{a+b}^{m+n} + a_{bc_{ak}}', 'images/subscript_multiple_characters.png')


if __name__ == '__main__':
    TestMethods().run()
    #TestMethods().testPara()
    #TestMethods().cauchysIntegralFormula()
    # TestMethods().testIntegral()
    TestMethods().testDotAndTilde()
    #fondi.MathText('a^b_c', 64, (255,255,255,255))
    #[('char', 'a'), ('bicmd', '^_'), ('arg', 'b'), ('arg', 'c')]

    #fondi.catchDoubleBiCommands([('char', 'a'), ('bicmd', '^'), ('arg', 'b'), ('bicmd', '_'), ('arg', 'c'), ('char', '+d')])

    #fondi.MathText('a^b_c', 64, (255,255,255,255))
    
    
    

