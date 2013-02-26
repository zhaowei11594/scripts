import com.sun.xml.internal.messaging.saaj.util.ByteOutputStream
import java.io.{File, FileOutputStream}
import java.net.URL
import java.util.regex.Pattern
import java.util.Scanner

object Appp  {

    case class StoredPage (URL : String, page_html : String)

    class Crawler {
        def openResourceInputStream(url : String) = {
            val connection = new URL(url).openConnection()
            connection.setRequestProperty("User-Agent", "Mozilla/5.0 (compatible;)")
            connection.connect()
            connection.getInputStream
        }

        def grabUrl(url : String) = {
            val pageScanner = new Scanner(openResourceInputStream(url))
            def getPage(res : String = "") : String = {
                if (pageScanner.hasNextLine) {
                    getPage(res + pageScanner.nextLine())
                }
                else {
                    res
                }
            }
            val imagePattern = Pattern.compile("""http:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&\?\/.=]+""")
            val matcher = imagePattern.matcher(getPage())
            def getHref(res : List[String] = List[String]()) : List[String] = {
                if (matcher.find()) {
                    getHref(res :+ matcher.group(0).toString())
                }
                else {
                    res
                }
            }
            getHref()
        }

    }
    
    def main(args : Array[String]) = {
        val crawler = new Crawler()
        println(crawler.grabUrl("http://ya.ru"))
        val sp = new StoredPage("Me", "So")
        println(sp.page_html)
    }

}
